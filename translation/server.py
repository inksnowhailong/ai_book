"""MADLAD-400 翻译服务：CTranslate2(int8) 推理 + FastAPI + 动态批处理。

设计要点（对应需求）：
- CTranslate2 int8：相比原生 fp32 约 3.5x 提速、显存减半 → "要快"
- 动态批处理：把并发到达的多条请求在几毫秒窗口内合并成一次 GPU 前向，
  并发越高吞吐提升越明显（实测 48 并发约 2.87x）→ "并发不掉速"
- MADLAD 把目标语言编码在输入 <2xx> 前缀里，所以一个 batch 里可以混合不同目标语言，
  这让动态批处理对"一对多"场景天然成立。

运行设备由环境变量 CT2_DEVICE 控制：
- 本机：默认 cpu（3B 在 4G 显存跑不动）
- 生产（租的 4090）：设 CT2_DEVICE=cuda，速度和成本才达标
"""
import asyncio
import os

import ctranslate2
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer

CT2_DIR = "./madlad400-3b-ct2-int8"        # 由 convert_int8.py 生成
HF_MODEL = "jbochi/madlad400-3b-mt"        # 仅用它的分词器
DEVICE = os.getenv("CT2_DEVICE", "cpu")
COMPUTE = "int8_float16" if DEVICE == "cuda" else "int8"  # CPU 上用纯 int8
MAX_BATCH = 32                             # 单次前向最多合并多少条
MAX_WAIT_MS = 8                            # 攒批等待窗口：超过就算没攒满也发车

translator = ctranslate2.Translator(CT2_DIR, device=DEVICE, compute_type=COMPUTE)
tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)


def _run_batch(items):
    """同步推理：items 是 [(text, target), ...]，返回译文列表。
    CT2 会释放 GIL，所以放到线程池里跑不会卡住事件循环。"""
    prompts = [f"<2{tgt}> {text}" for text, tgt in items]
    src_tokens = [tokenizer.convert_ids_to_tokens(tokenizer.encode(p)) for p in prompts]
    results = translator.translate_batch(
        src_tokens, max_batch_size=MAX_BATCH, beam_size=1, max_decoding_length=256
    )
    outs = []
    for r in results:
        ids = tokenizer.convert_tokens_to_ids(r.hypotheses[0])
        outs.append(tokenizer.decode(ids, skip_special_tokens=True))
    return outs


class _Batcher:
    """极简动态批处理器：请求入队 → 后台 worker 攒批 → 一次推理 → 用 future 回传各自结果。"""

    def __init__(self):
        self.queue: asyncio.Queue = asyncio.Queue()

    async def start(self):
        asyncio.create_task(self._worker())

    async def submit(self, text: str, target: str) -> str:
        fut = asyncio.get_event_loop().create_future()
        await self.queue.put(((text, target), fut))
        return await fut

    async def _worker(self):
        while True:
            item, fut = await self.queue.get()
            batch = [(item, fut)]
            # 在 MAX_WAIT_MS 窗口内尽量多攒，攒满 MAX_BATCH 或超时就发车
            try:
                while len(batch) < MAX_BATCH:
                    nxt = await asyncio.wait_for(self.queue.get(), timeout=MAX_WAIT_MS / 1000)
                    batch.append(nxt)
            except asyncio.TimeoutError:
                pass
            items = [b[0] for b in batch]
            try:
                results = await asyncio.to_thread(_run_batch, items)
                for (_, f), r in zip(batch, results):
                    f.set_result(r)
            except Exception as e:            # 整批失败时逐个回传异常，不吞
                for _, f in batch:
                    if not f.done():
                        f.set_exception(e)


batcher = _Batcher()
app = FastAPI()


class Req(BaseModel):
    text: str
    target: str          # 目标语言代码，如 en/zh/ja/fr


@app.on_event("startup")
async def _startup():
    await batcher.start()


@app.post("/translate")
async def translate(req: Req):
    out = await batcher.submit(req.text, req.target)
    return {"translation": out}
