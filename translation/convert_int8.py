"""把 F32 的 MADLAD-3B 转成 CTranslate2 int8（约 11.8GB → ~3GB）。

用法（推荐在云端免费 GPU 环境跑，网快）：
  下载 F32 → 转成 int8 → 把产出的 madlad400-3b-ct2-int8/ 文件夹打包下载回本地存。
  这样只在云端下一次 12G，本地永远只留 3G 的自包含成品，离线可跑。

- 纯 CPU 过程，不用显卡；转换时会把模型载入内存（约 12G），48G 内存没问题。
- 产物是一个自包含文件夹 madlad400-3b-ct2-int8/，就是 server.py 里 CT2_DIR 指向的东西。
- 量化用纯 int8：本机 CPU 上最合适（int8_float16 的 float16 在 CPU 是软件模拟、偏慢）；
  这份 int8 成品同一份将来直接上 4090 也能用，一举两得。
"""
import subprocess
import sys

MODEL = "jbochi/madlad400-3b-mt"
OUT = "madlad400-3b-ct2-int8"

cmd = [
    "ct2-transformers-converter",
    "--model", MODEL,
    "--output_dir", OUT,
    "--quantization", "int8",
    "--force",  # 允许覆盖已存在的输出目录
]
print("运行：", " ".join(cmd), "\n")
sys.exit(subprocess.call(cmd))
