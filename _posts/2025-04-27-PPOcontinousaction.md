---
title: 连续动作空间 PPO求解
description: 这个博客是作者做完离散PPO，现在来尝试连续PPO写下的博客。还没看，这是我在探索PPO求解连续动作空间问题时候找到的一篇博客。希望有所帮助。这个博主应该很有意思。
author: Chen Zhang
date: 2025-04-27 00:00:00 +0800
categories: [Blogging]
tags: [Reinforcement Learning, PPO, Continuous Action Space]
pin: true
math: true
mermaid: true
---

[原文链接 - Policy-based Methods for a Continuous Action Space](https://medium.com/geekculture/policy-based-methods-for-a-continuous-action-space-7b5ecffac43a)

**要点总结：**
- 文中提到为什么基于价值的RL（如Q-Learning）不适合用来求解连续动作空间。Q-Learning方法让智能体学习每个动作的Q值，并选择使Q值最大的动作，这只适用于离散动作空间，因为连续动作空间中的动作无限多，无法遍历。
- 文中提到了稀疏奖励问题，但没看出来他具体怎么解决的，或许是没看仔细。
- 文中还给出了一个和一篇文章相反的结论，在这个博客中博主得出了连续PPO强于离散PPO，令我手足无措！