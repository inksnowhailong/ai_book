# MADLAD-400 翻译服务（学习 + 自建实践）

把一个开源翻译模型跑起来、量化提速、包成服务，用来对比"自建 vs 直接用 Gemini API"的真实取舍。
翻译只是教具，真正学到的是**下载→量化→部署→压测**这套可迁移的手艺。

## 选型结论（为什么是这套）

| 决策 | 选择 | 原因 |
|---|---|---|
| 模型 | **MADLAD-400-3B** | 准确度在 XCOMET 上超 GPT-4，Apache-2.0 商用干净，419 语言一对多原生 |
| 推理引擎 | **CTranslate2 int8** | 相比 fp32 约 3.5x 提速、显存减半 |
| 服务框架 | **FastAPI + 动态批处理** | 把并发请求合并成一次前向，高并发吞吐再翻倍 |
| 破冰验证 | 本机 **CPU** | 本机 GTX 1650 只有 4G 显存，装不下 3B；CPU 慢但够验证质量 |
| 生产 | **租 4090（CT2_DEVICE=cuda）** | 全天有流量、喂饱一张卡，单条成本把 API 打到骨折 |

## 本机能力判定（GTX 1650 4G / 48G 内存 / i7-10700）

```
下载 F32 本体(11.8G)      ✅  磁盘足够
转换成 CT2 int8           ✅  纯 CPU + 内存，48G 绰绰有余
CPU 上跑通(验证质量)      ✅  慢（每句几秒），只够验证不够生产
GPU 上跑 MADLAD-3B        ❌  4G 显存装不下 3B，必爆 → 想用 GPU 得换 NLLB-600M
```

## 环境

已装 **Python 3.12.10**，项目用独立 venv，不污染系统。

```bash
# 在 translation/ 目录下
.venv\Scripts\activate            # 激活虚拟环境（Windows）
pip install -r requirements.txt   # 装依赖（首次约几百 MB）
```

## 四步流程

```bash
# ① 破冰：在你真实文本上验证质量（改 translate_min.py 里的 samples！）
python translate_min.py

# ② 质量满意后，转成 int8（约 12G → 3G，纯 CPU，约几分钟）
python convert_int8.py

# ③ 起服务
uvicorn server:app --host 0.0.0.0 --port 8000

# ④ 另开终端压测：量单条延迟 + 并发吞吐
python benchmark.py
```

## 上生产（租 4090 时）

同样四步，唯一区别是第 ③ 步设备切 GPU：

```bash
CT2_DEVICE=cuda uvicorn server:app --host 0.0.0.0 --port 8000
```

## 常用目标语言代码（MADLAD 的 `<2xx>`）

`en` 英 · `zh` 中 · `ja` 日 · `ko` 韩 · `fr` 法 · `de` 德 · `es` 西 · `ru` 俄 · `pt` 葡 · `ar` 阿 · `th` 泰 · `vi` 越
（完整 419 种见模型卡）

## 备选：想在本机用上 GPU

MADLAD-3B 本机 GPU 跑不了。若想让 GTX 1650 真正加速，把模型换成
`facebook/nllb-200-distilled-600M`（int8 约 0.7G 显存，1650 能带），质量比 MADLAD 低一档。
