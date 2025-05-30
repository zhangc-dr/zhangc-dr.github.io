---
title: DRL相关资料
description: 强化学习相关的资料。
author: Chen Zhang
date: 2025-04-27 00:00:00 +0800
categories: [Blogging]
tags: [Reinforcement Learnings]
pin: true
math: true
mermaid: true
---

**General Reinforcement Learning & Policy Gradients:**
- [Stable Baselines3 Distributions文档](https://stable-baselines3.readthedocs.io/en/master/common/distributions.html): Documentation on action distributions in Stable Baselines3.
- [Spinning Up in Deep RL](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html): An OpenAI guide to policy gradients, especially useful for beginners. Parts 1, 2, and 3 explain the step-by-step implementation of policy gradient updates, covering topics like reward-to-go (R), baselines, and the advantage function (using Q(st,at) and V(st)).
- [Farama Gymnasium: Create Custom Env 官方教程](https://gymnasium.farama.org/introduction/create_custom_env/): 本教程提供了一个基于 gym 构建自定义环境的规范模板，适合作为后续自定义 RL 环境的参考。

**PPO Implementation & Details:**
- [CleanRL - Overview](https://docs.cleanrl.dev/rl-algorithms/ppo/#experiment-results_7): PPO overview and experiment results from CleanRL documentation.
- [The 37 Implementation Details of Proximal Policy Optimization](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/): A blog post detailing various PPO implementation specifics.
- [ppo_continuous_action github](https://github.com/vwxyzjn/ppo-implementation-details/blob/main/ppo_continuous_action.py): Example PPO implementation for continuous action spaces.

**Key Papers & Concepts:**
- [High-Dimensional Continuous Control Using Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438): The paper introducing Generalized Advantage Estimation (GAE), providing its definition and derivation.
- [Deterministic Policy Gradient Algorithms](https://proceedings.mlr.press/v32/silver14.pdf): This paper formally defines stochastic and deterministic policies and their update methods.

**Community Resources & Tutorials:**
- [PPO知识点梳理 代码 (尽我可能细致通俗解释！)](https://www.cnblogs.com/myleaf/p/18595876): A personal blog post offering a detailed explanation of PPO, with code examples (including Python progress bars) and theoretical explanations based on Li Hongyi's lectures.

**个人思考与补充记录（2025年4月28日补充）：**
- 我正在寻找高斯分布是否是PPO算法求解连续动作空间有效方法的有关论证。幸运的是，找到了一篇文章说了用离散动作空间去近似连续动作空间，然后再用离散动作空间的求解方法去求，网络就用softmax（这篇文章叫Discretizing Continuous Action Space for On-Policy Optimization，在ToolBook/PAPER文件夹中）。但是不幸的是，还没有找到高斯分布的替代分布。

- 4月28日回头来看这条日志，发现没记录清楚，我没说为什么没到到高斯分布的替代分布是不辛的，以及为什么要替代高斯分布。这两个问题其实是一个问题，我来回答一下为什么要替代高斯分布。我觉得应该用离散问题来解释这个问题比较容易点，因为连续动作的‘概率’其实是概率密度，是一个相比于我们常说的明天下雨的概率是50%更加抽象的问题。
- 我经常给我对象讲这么一个例子：有2个待选的目的地，现在要去往两个目的地之一，去往这两个目的地可能会收获钱但也有可能被抢钱，事先你是知道哪里会被抢哪里能收获钱的。怎么规划去哪个地方才能收获最多的钱呢？对于正常人一秒就能给出答案，只去收获钱的那家不就是最优的方案吗。但是现在问题来了，小明不是正常人，他只会摇色子，他现在求着你让你帮他做一个特制的色子，好让他拿最多的钱。这个问题对你来说其实也是个简单的问题，给他一个全是六点的色子，告诉他投中六就去甲地（收获钱的地方），投中别的点就去乙地（被抢钱的地方或者比甲地收获的钱少）。坏了！我好像跑题了，我好像要讲为什么要替代高斯分布的。也没完全跑题，刚刚这个问题是不是相当于把问题构建成了一个概率的优化的问题，去甲地的概率假设记作P1，去乙地的概率记作P2，去甲地能收获的钱记作R1，去乙地能收获的钱记作R2，现在要最大化P1*R1+P2*R2，优化变量是P1和P2.对于刚刚小明这个问题很显然，P1=1，P2=0，这时候最优。这就是随机策略。随机策略的核心我目前理解的就是设计一个骰子，这个骰子可能很奇特，有你能做的选项数那么多个面，但是每个面不一定长的一样，这样就可以保证每个面的概率不一样了嘛。对于一个一般的随机策略问题，可以理解成，你现在有很多很奇怪的骰子，骰子的面还是和动作选项数一样，你每次在环境中某个状态下需要接着往下走的时候，你就掏出一枚这个状态下的骰子，就根据他的指示去Move，最终你回头看你会发现，你一路上收获的奖励真不少。算了还没进入正题！改天再写。
> 目前没找到比高斯分布更合适的替代分布，也没有找到关于高斯分布是否最优的权威论证。
{: .prompt-warning }

> 相关论文：Discretizing Continuous Action Space for On-Policy Optimization（见ToolBook/PAPER文件夹）。
{: .prompt-tip }

**后续计划**  
后续需继续探索高斯分布之外的策略分布，及其在PPO等算法中的表现和理论依据。