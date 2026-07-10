"""基准脚本：量两个你最关心的数——单条延迟 和 并发吞吐。

跑之前先启动服务：  uvicorn server:app --host 0.0.0.0 --port 8000
然后另开一个终端跑： python benchmark.py
"""
import asyncio
import time

import httpx

URL = "http://localhost:8000/translate"
SAMPLE = {"text": "我们社区今晚有一场直播，欢迎来看。", "target": "en"}


async def one(client):
    t = time.perf_counter()
    r = await client.post(URL, json=SAMPLE)
    return time.perf_counter() - t, r.json()["translation"]


async def main():
    async with httpx.AsyncClient(timeout=120) as client:
        await one(client)  # 预热

        # 单条延迟：串行 10 次取平均
        lat = [(await one(client))[0] for _ in range(10)]
        print(f"单条延迟：平均 {sum(lat) / len(lat) * 1000:.0f}ms  最快 {min(lat) * 1000:.0f}ms")

        # 并发吞吐：一次性打 N 条，看总耗时和 QPS
        for n in (8, 32, 64):
            t = time.perf_counter()
            await asyncio.gather(*[one(client) for _ in range(n)])
            dt = time.perf_counter() - t
            print(f"并发 {n:>3}：总耗时 {dt:.2f}s  →  {n / dt:.1f} 条/秒")


if __name__ == "__main__":
    asyncio.run(main())
