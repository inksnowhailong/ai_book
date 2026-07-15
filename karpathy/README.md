# Karpathy — Neural Networks: Zero to Hero 学习目录

Andrej Karpathy（前 OpenAI 创始成员、前特斯拉 AI 总监）的免费视频系列：从零手写神经网络，终点是亲手写出一个 GPT。
全程一个人现场敲代码，讲解密度极高，没有废话。

- 课程主页：https://karpathy.ai/zero-to-hero.html
- YouTube 播放列表：https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ
- 注意：**这套课的灵魂在视频里**，配套仓库只有代码没有讲解正文，必须跟着视频看。

## 视频清单

| # | 标题 | 时长 | 讲什么 | 配套仓库 |
|---|---|---|---|---|
| 1 | [micrograd：反向传播彻底讲透](https://www.youtube.com/watch?v=VMj-3S1tku0) | 2.5h | 手写一个约 100 行的自动求导引擎，神经网络训练的核心（backprop）从此不是黑盒 | [micrograd](https://github.com/karpathy/micrograd) |
| 2 | [makemore ①：语言模型入门](https://www.youtube.com/watch?v=PaCmpygFfXo) | 2h | 做一个"起名字"的字符级语言模型，从最土的 bigram 统计到第一个神经网络版本 | [makemore](https://github.com/karpathy/makemore) |
| 3 | [makemore ②：MLP](https://www.youtube.com/watch?v=TCH_1BHY58I) | 1.5h | 升级成多层感知机，引入 embedding、超参调优、训练/验证/测试集划分 | 同上 |
| 4 | [makemore ③：激活值、梯度与 BatchNorm](https://www.youtube.com/watch?v=P6sfmUTpUmc) | 2h | 深网络为什么难训：激活饱和、梯度消失，以及 BatchNorm 怎么救 | 同上 |
| 5 | [makemore ④：成为 backprop 忍者](https://www.youtube.com/watch?v=q8SA3rM6ckI) | 2h | 不用 autograd，徒手推导反向传播的每一行梯度。全系列含金量最高、最疼的一集 | 同上 |
| 6 | [makemore ⑤：WaveNet](https://www.youtube.com/watch?v=t3YJ5hKiMQ0) | 1h | 把 MLP 加深成树状卷积结构（WaveNet），顺便看 PyTorch 的 API 设计哲学 | 同上 |
| 7 | [Let's build GPT：从零手写 GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) | 2h | 从空文件写出完整 GPT：self-attention、transformer block 全部手写，训出莎士比亚腔生成器。**全系列之魂** | [ng-video-lecture](https://github.com/karpathy/ng-video-lecture) / [nanoGPT](https://github.com/karpathy/nanoGPT) |
| 8 | [GPT Tokenizer：手写 BPE 分词器](https://www.youtube.com/watch?v=zduSFxRajkE) | 2h | 手写 BPE 算法——平时调的 `tokenizer` 的内脏，也是 LLM 很多诡异行为的根源 | [minbpe](https://github.com/karpathy/minbpe) |
| 9 | [复现 GPT-2 (124M)](https://www.youtube.com/watch?v=l8pRSuU81PU) | 4h | 加餐：从零复现 GPT-2 的完整训练，含混合精度、分布式训练等工程实战 | [build-nanogpt](https://github.com/karpathy/build-nanogpt) |

## 跟法

1. 前置：fastai Part 1 的 04、05 笔记本跑完（有梯度下降手感）再开这套，第 1 集会顺很多。
2. 看视频必须**同步敲代码**——暂停、自己写、对答案；只看不敲等于白看。
3. 每集敲完的 notebook 存进本目录，一集一个文件。
4. 第 5 集（backprop 忍者）最疼，卡住是正常的，别在这弃坑。
5. 与 Qwen3Guard 实战的接口：第 7 集写完 attention 后，回头看 moderation/ 里"抓 label 位置 logits 做 softmax"的方案，应能自己实现。

## 进度

- [ ] 1 micrograd
- [ ] 2 makemore ① bigram
- [ ] 3 makemore ② MLP
- [ ] 4 makemore ③ BatchNorm
- [ ] 5 makemore ④ backprop 忍者
- [ ] 6 makemore ⑤ WaveNet
- [ ] 7 Let's build GPT
- [ ] 8 Tokenizer
- [ ] 9 复现 GPT-2（选修）
