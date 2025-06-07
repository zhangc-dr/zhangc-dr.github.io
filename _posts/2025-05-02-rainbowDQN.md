---
title: Rainbow DQN的介绍，另外整理DQN/DDQN/Dueling DQN原理
description: 其实对于DQN的改进不止Double和Dueling这两种，还有priority/multi-step/distribution/noisy，加上DQN本身一共7种DQN算法，把这7种算法结合起来就被称为彩虹DQN。目前我还需要去弄明白这几种改进思路。另外，今天才意识到要去看这三个算法出处，他们各自对应了一篇论文。他们的题目分别是 Human-level control through deep reinforcement learning, Deep Reinforcement Learning with Double Q-learning, Dueling Network Architectures for Deep Reinforcement Learning 待整理!
author: Chen Zhang
date: 2025-05-02 00:00:00 +0800
categories: [DRL]
tags: [DQN, Rainbow DQN]
pin: true
math: true
mermaid: true
---

[arXiv: Rainbow: Combining Improvements in Deep Reinforcement Learning](https://arxiv.org/pdf/1710.02298)

本笔记简要介绍了Rainbow DQN算法，以及DQN、Double DQN、Dueling DQN的原理。Rainbow DQN结合了7种DQN相关改进（包括priority、multi-step、distribution、noisy等），是对DQN家族的集大成者。目前还需进一步梳理各个改进的具体思路及其对应的原始论文：

- DQN: Human-level control through deep reinforcement learning
- Double DQN: Deep Reinforcement Learning with Double Q-learning
- Dueling DQN: Dueling Network Architectures for Deep Reinforcement Learning

> 待整理详细内容。
{: .prompt-warning }
