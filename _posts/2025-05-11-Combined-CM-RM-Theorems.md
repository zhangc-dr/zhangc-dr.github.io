---
title: Contraction Mapping theorem和Robbins Monro theorem
description: 这个博客主要介绍了Contraction Mapping theorem和Robbins Monro theorem。Contraction Mapping theorem用于判断递归数列的收敛性及求解其收敛值。Robbins Monro theorem则用于通过迭代方式求解逼近期望的统计均值或非线性方程的根。
author: Chen Zhang
date: 2025-05-11 00:00:00 +0800
categories: [Blogging]
tags: [Mathematics]
pin: true
math: true
mermaid: true
---

## Contraction Mapping Theorem

可以参考知乎文章[压缩映射原理](https://zhuanlan.zhihu.com/p/458151225)。

**要点总结：**
- 简单的讲，条件就是对于$f(x)$在定义域上必须满足导数的绝对值小于1。
- 算法是：$x_{k+1}=f(x_k)$，代码如下：

```matlab
%% Contraction Mapping algorithm: existence, uniqueness, algorithm of an equation's root
% function: f(x) = 1/x + 1, x>1; Utilizing contraction mapping theorem, we can
% obatain the root of equation f(x) = x, which is unique and available.
k = 0; x = 1; done = false;
while ~done
    k = k + 1;
    x_ = 1/x + 1;
    done = norm(x-x_)<1e-5;
    x = x_;
    disp(['k: ',num2str(k),', estimate: ',num2str(x)])
end
```

---

## Robbins Monro Theorem

参考CSDN文章[Robbins-Monro(RM)算法【随机近似】](https://blog.csdn.net/v20000727/article/details/138076216)。

**要点总结：**
- 这个算法要收敛，对函数的要求其实蛮高的，第一个条件要求函数$g(x)$的导数为正且不能为+∞，这就是说要求函数是单调递增的。
- 要求步长为消失步长，常见的消失步长如 $ak=1/k$。
- 对噪声的要求，要求噪声不能太离谱。
- 博客给出了Robbins Monro的算法和Newton method的算法，
$$
\begin{align}
RM: {x_{k + 1}} \leftarrow {x_k} - {\alpha _k}f({x_k}), \\
Newton: {x_{k + 1}} \leftarrow {x_k} - f({x_k})/f'({x_k}),
\end{align}
$$
代码如下。

```matlab
%% 1.Robbins Monro algorithm: nonlinear equation
% equation: lnx - 1 = 0
k = 0; x = 1; done = false;
while ~done
    k = k + 1; a = 1/(k+1);
    x_ = x - a*(log(x)-1);
    done = norm(x-x_)<1e-5;
    x = x_;
    disp(['k: ',num2str(k),', estimate: ',num2str(x)])
end
```
```matlab
%% 2. Newton algorithm: nonlinear equation
% equation: lnx - 1 = 0
x = 1; done = false; k = 0;
while ~done
    k = k + 1;
    x_ = x -(log(x)-1)*x;
    done = norm(x-x_)<1e-5;
    x = x_;
    disp(['k: ',num2str(k),', estimate: ',num2str(x)])
end
```
```matlab
%% 3.Robbins Monro algorithm: expectation estimatimation 
% equation: uk - u = 0, where f(x) = e^x, x~Uniform(0,1), u = E{f(x)}
k = 0; u = -1; done = false;
while ~done
    k = k + 1; a = 1/(k+1);
    fx = exp(rand);
    u_ = u - a*(u - fx);
    done = norm(u-u_)<1e-6;
    u = u_;
    disp(['k: ',num2str(k),', estimate: ',num2str(u)])
end
```
- 博客还讲到了如何使用Robbins Monroe theorem求优化问题：优化问题可以转换成求目标函数的极值点，极值点可以用对函数求一阶导来得到，然后令一阶导等于0，这就构造出了一个方程求根的问题。对于这个问题如果满足Robbins Monro的条件，就可以使用Robbins Monro定理迭代得到方程的根，而且定理还能保证迭代出来的根最终一定能收敛到真实值。
