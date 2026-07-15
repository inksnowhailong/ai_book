# fast.ai — Practical Deep Learning for Coders 学习目录

## fastbook 20 章概览（阅读主粮，在 [../fastbook/](../fastbook/)；中英对照版在 [../fastbook-zh/](../fastbook-zh/)）

优先级：⭐ 主动脉必读 / ○ 按需 / △ 可跳过或最后看

| 章 | 标题 | 讲什么 | 优先级 |
|---|---|---|---|
| 01 | Your Deep Learning Journey | 全景开篇：什么是机器学习（Arthur Samuel 定义）、训第一个图像分类器、迁移学习为什么有效、术语表 | ⭐ |
| 02 | From Model to Production | 从想法到上线：自建数据集、数据清洗、部署成 Web 应用、上线后会翻车的坑（数据漂移、反馈回路） | ⭐ |
| 03 | Data Ethics | 数据伦理：反馈回路放大偏见、模型出错谁负责。审核系统的人尤其该翻一遍 | ○ |
| 04 | Under the Hood: Training a Digit Classifier | **全书心脏**（349 格最厚）：用 MNIST 手写数字从零讲透张量、梯度下降、损失函数、SGD——"训练"二字的全部内幕 | ⭐ |
| 05 | Image Classification | 图像分类完整流程：数据块 API、学习率查找器、判别式学习率、交叉熵损失的逐步拆解 | ⭐ |
| 06 | Other Computer Vision Problems | 多标签分类与回归：一张图多个标签时损失函数怎么变（对照审核系统"一条内容命中多个违规类别"） | ○ |
| 07 | Training a State-of-the-Art Model | 冲榜技巧：归一化、渐进式缩放、TTA、mixup、标签平滑 | ○ |
| 08 | Collaborative Filtering Deep Dive | 推荐系统：协同过滤、embedding 的第一次正式登场——"把离散的东西变成向量"这个思想后面 NLP 全靠它 | ○ |
| 09 | Tabular Modeling Deep Dive | 表格数据（300 格）：随机森林、特征重要性、神经网络处理表格。用户行为分析就是这类 | ○ |
| 10 | NLP Deep Dive: RNNs | **NLP 主战场**：文本怎么变数字（tokenization、numericalization）、语言模型微调做分类——Qwen3Guard 的直系祖先 | ⭐ |
| 11 | Data Munging with fastai's Mid-Level API | fastai 中层 API 的数据加工术，框架味重 | △ |
| 12 | A Language Model from Scratch | 从零手写语言模型：RNN → LSTM 一步步搭出来，理解"模型怎么记住上文" | ⭐ |
| 13 | Convolutional Neural Networks | 卷积从零讲透：卷积核到底在算什么、感受野、1cycle 训练 | ○ |
| 14 | ResNets | 残差连接：为什么"跳过几层"这个小改动让深网络变得可训——现代所有大模型都有它的血 | ○ |
| 15 | Application Architectures Deep Dive | 各任务架构对比拆解（视觉/NLP/表格），架构选型的判断力来源 | ○ |
| 16 | The Training Process | 优化器内幕：momentum、Adam、weight decay，以及训练回调机制 | ○ |
| 17 | A Neural Net from the Foundations | 深水区：纯 Python 手写矩阵乘法、前向反向传播——fastai 版的"Karpathy 体验" | ○ |
| 18 | CNN Interpretation with CAM | 可解释性：CAM 热力图看模型"在看哪里"——回答"模型为什么这么判" | △ |
| 19 | A fastai Learner from Scratch | 从零重造 fastai 的 Learner：给工程师的框架设计课 | △ |
| 20 | Concluding Thoughts | 收尾寄语，7 格，五分钟 | △ |
