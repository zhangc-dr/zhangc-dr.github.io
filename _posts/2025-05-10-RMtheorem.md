---
title: Robbins Monro theorem和Robbins Monro algorithm
description: 这个博客把赵世钰老师第六章中一部分内容单独拎出来详细介绍了一下，提到了如何用迭代的方式求解逼近期望的统计均值。这个定理还能被用于求解非线性方程的根，要想使用这个定理要求也很多。
author: Chen Zhang
date: 2025-05-10 00:00:00 +0800
categories: [Blogging]
tags: [Mathematics, Robbins-Monro, Stochastic Approximation]
pin: true
math: true
mermaid: true
---

[CSDN 原文](https://blog.csdn.net/v20000727/article/details/138076216)

**要点总结：**
- 这个算法要收敛，对函数的要求其实蛮高的，第一个条件要求函数g(x)的导数为正且不能为+∞，这就是说要求函数是单调递增的。
- 要求步长为消失步长，常见的消失步长如 ak=1/k。
- 对噪声的要求，要求噪声不能太离谱。
- 博客给出了Robbins Monro的算法和Newton method的算法，见 Formula 4，代码实现见本地 D:\research\MatlabCode\MyTry\others\someAlgorithm.m。
- 博客还讲到了如何使用Robbins Monroe theorem求优化问题：优化问题可以转换成求目标函数的极值点，极值点可以用对函数求一阶导来得到，然后令一阶导等于0，这就构造出了一个方程求根的问题。对于这个问题如果满足Robbins Monro的条件，就可以使用Robbins Monro定理迭代得到方程的根，而且定理还能保证迭代出来的根最终一定能收敛到真实值。