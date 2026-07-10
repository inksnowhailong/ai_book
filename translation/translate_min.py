"""破冰脚本：用原生 transformers 加载 MADLAD-400-3B，在你自己的文本上翻几句。

目的：先确认「模型翻译质量对你的社区文本够不够好」，再谈优化与上生产。
本机说明：GTX 1650 只有 4G 显存，装不下 3B 模型，所以固定用 CPU 跑。
         慢（每句几秒）是正常的——这一步只为验证质量，不追求速度。
"""
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# jbochi 的 F32 移植版：transformers 现成可加载（原 google 官方是 T5X 格式，麻烦）
MODEL = "jbochi/madlad400-3b-mt"
DEVICE = "cpu"

print(f"[1/2] 加载 {MODEL} 到 {DEVICE} …（首次运行会下载约 12GB，请耐心等）")
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL, torch_dtype=torch.float32).to(DEVICE)
print("[2/2] 加载完成，开始翻译\n")


def translate(text: str, target: str) -> str:
    """把 text 翻成目标语言 target（如 en/ja/fr/es/ko）。
    MADLAD 用法：在原文前加 <2xx> 目标语言标记，源语言由模型自动识别。
    """
    prompt = f"<2{target}> {text}"
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    out = model.generate(**inputs, max_new_tokens=256, num_beams=1)  # 贪心解码，快
    return tokenizer.decode(out[0], skip_special_tokens=True)


if __name__ == "__main__":
    # ⭐ 把下面换成你【真实的社区文本】，才测得出这模型对你有没有用
    samples = [
        ("我们社区今晚有场自动驾驶直播，来看看呗", "en"),
        ("这个功能也太顶了，爱了爱了", "ja"),
        ("求助：有没有人遇到过登录一直转圈的？", "fr"),
    ]
    for text, tgt in samples:
        print(f"[{tgt}] 原文：{text}")
        print(f"     译文：{translate(text, tgt)}\n")
