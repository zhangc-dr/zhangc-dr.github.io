---
title: 文章整理。
description: 本文汇总了现有文献对RSMA优于NOMA和SDMA的表述，以及从哪些角度进行对比，如何呈现出RSMA的优势。
author: Chen Zhang
date: 2025-06-10 14:19:00 +0800
categories: [Papers]
tags: [RSMA, NOMA, SDMA]
pin: false
math: true
mermaid: true
---

## Paper1: [On Performance of Downlink THz-Based Rate-Splitting Multiple-Access (RSMA): Is it Always Better Than NOMA?](https://arxiv.org/abs/2305.07361) - Thai-Hoc Vu
### 1. 文章所要解决的核心问题

|Problems|
|--|
|(1). The study on outage probability (OP) and throughput analyses remain unexplored due to the complex nature of the precoder design, making it challenging to find optimal closed-form solutions as to prior optimization works.|
|(2). The superiority of RSMA over its counterparts in terms of OP and throughput has not been clarified in the literature.|
|(3). The existing literature on RSMA has mostly focused on simplified models with fixed user locations that cannot realistically characterize user movement behavior, such as indoor-mobile networks, vehicle-to-infrastructure (V2I) communications, or air-to-ground (A2G) communications.|

### 2. 正文部分
#### 1. 文中列举了RSMA在现实中的应用场景
|Application|
|--|
|(1). In multimedia broadcast/multicast services, the common stream delivers shared content like videos or audio, while private streams provide personalized data such as subtitles or feedback.|
|(2). In joint sensing and communication systems, sensor acquisition requests are sent via the common stream, whereas user-specific communication messages are carried by private streams.|
|(3). In machine-type communication networks, control information is transmitted over the common stream, while secure data like sensor readings or commands are sent through private streams.|
|(4). In vehicular networks, the common stream shares group messages like safety alerts, while the private stream ensures secure delivery of personal data such as certificates or signatures.|

#### 2. RSMA发射信号的定义
The transmit signal is $x = \sqrt {{\alpha_c}{P_t}} {{\bf{w}}_{c} }{s_c} + \sum\limits_k {\sqrt {{\alpha _k}{P_t}} {{\bf{w}}_k}{s_k}} $, where  $P_t$ is the transmit power, ${{\bf{w}}_{c} },{{\bf{w}}_k}$ are the precoding weights for $s_c,s_k$, with ${\left\| {{{\bf{w}}_{c} }} \right\|^2} = {\left\| {{{\bf{w}}_k}} \right\|^2} = 1$. And $\alpha_c$, $\alpha_k$ denote the power allocation coefficients of $s_c$ and $s_k$, respectively, with ${\alpha _c} + \sum\limits_k {{\alpha _k}}  = 1$.

#### 3. 文中考虑1-layer RS以及imperfect SIC
该部分需要了解作者这样书写表达的优点，以及了解如何建模imperfect SIC.
The channel model is based on Rayleigh model, which ${\bf{h}}_k=\sqrt{\beta_k}{\bf{g}}_k$.
The SINRs to decode $s_c$ and $s_k$ are respectively expressed as
$$
\begin{aligned}
\gamma _c^k &= \frac{{{\alpha _c}\rho {\beta _k}{{\left| {{{\bf{g}}^H_k}{{\bf{w}}_{\mathop{\rm c}\nolimits} }} \right|}^2}}}{{\sum {{\alpha _j}\rho {\beta _k}{{\left| {{{\bf{g}}^H_k}{{\bf{w}}_j}} \right|}^2}}  + 1}},\\
\gamma _p^k &= \frac{{{\alpha _k}\rho {\beta _k}{{\left| {{{\bf{g}}^H_k}{{\bf{w}}_k}} \right|}^2}}}{{\varsigma {\alpha _c}\rho {\beta _k}{{\left| {{{\bf{g}}^H_k}{{\bf{w}}_c}} \right|}^2} + \sum\nolimits_{j \ne k} {{\alpha _j}\rho {\beta _k}{{\left| {{{\bf{g}}^H_k}{{\bf{w}}_j}} \right|}^2}}  + 1}},
\end{aligned}
$$
where $\varsigma \in [0,1)$ is the imperfect factor and $\rho = P/\sigma^2$.

#### 4. 如何基于ZF方法设计公有和私有信息
ZF的目的是尽可能消除MUI，以Nt天线基站和K单天线用户的SDMA系统为例，第k个用户解码自己信息的信噪比：

$$
\gamma _k = \frac{{{\alpha _k}\rho {\beta _k}{{\left| {{{\bf{g}}^H_k}{{\bf{w}}_k}} \right|}^2}}}{{\sum_{j \ne k} {{\alpha _j}\rho {\beta _k}{{\left| {{{\bf{g}}^H_k}{{\bf{w}}_j}} \right|}^2}}  + 1}}.
$$

ZF会要求 $ {\bf{g}}^H_k{\bf{w}}_j=0,\forall j \ne k, {\bf{g}}^H_k{\bf{w}}_k=\left| {\bf{g}}_k\right|$. 那么要如何得到这个${\bf{w}}_k$呢？
首先，把所有gk和wk分别合成一个矩阵${\bf{G}}{\rm{ = }}\left[ {{{\bf{g}}_1},{{\bf{g}}_2}, \cdots ,{{\bf{g}}_K}} \right] \in {C^{Nt \times K}},{\bf{W}} = \left[ {{{\bf{w}}_1},{{\bf{w}}_2}, \cdots ,{{\bf{w}}_K}} \right] \in {C^{Nt \times K}}$. 然后有

$$
{\mathbf{G}}^H{\mathbf{W}} = \begin{bmatrix}
{\mathbf{g}}_1^H \\
{\mathbf{g}}_2^H \\
\vdots \\
{\mathbf{g}}_K^H
\end{bmatrix}
\begin{bmatrix}
{\mathbf{w}}_1 & {\mathbf{w}}_2 & \cdots & {\mathbf{w}}_K
\end{bmatrix} 
= \begin{bmatrix}
{\mathbf{g}}_1^H{\mathbf{w}}_1 & {\mathbf{g}}_1^H{\mathbf{w}}_2 & \cdots & {\mathbf{g}}_1^H{\mathbf{w}}_K \\
{\mathbf{g}}_2^H{\mathbf{w}}_1 & {\mathbf{g}}_2^H{\mathbf{w}}_2 & \cdots & {\mathbf{g}}_2^H{\mathbf{w}}_K \\
\vdots & \vdots & \vdots & \vdots \\
{\mathbf{g}}_K^H{\mathbf{w}}_1 & {\mathbf{g}}_K^H{\mathbf{w}}_2 & \cdots & {\mathbf{g}}_K^H{\mathbf{w}}_K
\end{bmatrix} 
\\
= \begin{bmatrix}
\left| {\mathbf{g}}_1 \right| & 0 & \cdots & 0 \\
0 & \left| {\mathbf{g}}_2 \right| & \cdots & 0 \\
\vdots & \vdots & \vdots & \vdots \\
0 & 0 & \cdots & \left| {\mathbf{g}}_K \right|
\end{bmatrix} 
= \text{diag}\left( \left[ \left| {\mathbf{g}}_1 \right|, \left| {\mathbf{g}}_2 \right|, \cdots, \left| {\mathbf{g}}_K \right| \right] \right)
$$

那么如何求解W呢？这就是一个线性代数问题了，然而很明显这个方程无解或者无唯一解，无法通过以前理解的现代知识求解。这里就需要引入伪逆。那么W就为
$$
{\bf{W}} = {\rm{pinv}}({{\bf{G}}^H})diag\left( {\left[ {\left| {{{\bf{g}}_1}} \right|,\left| {{{\bf{g}}_2}} \right|, \cdots ,\left| {{{\bf{g}}_K}} \right|} \right]} \right),
$$

根据[The Matrix Cookbook](http://matrixcookbook.com)书中第21页可以求出${\rm{pinv}}({{\bf{G}}^H}) = {\bf{G}}{({{\bf{G}}^H}{\bf{G}})^{ - 1}}$，故
$$
{\bf{W}} = {\bf{G}}{({{\bf{G}}^H}{\bf{G}})^{ - 1}}diag\left( {\left[ {\left| {{{\bf{g}}_1}} \right|,\left| {{{\bf{g}}_2}} \right|, \cdots ,\left| {{{\bf{g}}_K}} \right|} \right]} \right).
$$
这就是wk的求解全过程了。

在RSMA中由于引入了新的待优化变量wc使得问题变得更加复杂。要想完全消除干扰，在$\gamma_c^k$中需要满足$ {\bf{g}}^H_k{\bf{w}}_j=0,\forall j, {\bf{g}}^H_k{\bf{w}}_c=\left| {\bf{g}}_k\right|$；在$\gamma_p^k$中需要满足$ {\bf{g}}^H_k{\bf{w}}_c={\bf{g}}^H_k{\bf{w}}_j=0,\forall j \ne k, {\bf{g}}^H_k{\bf{w}}_k=\left| {\bf{g}}_k\right|$。而${\bf{g}}^H_k{\bf{w}}_k=\left| {\bf{g}}_k\right|$和${\bf{g}}^H_k{\bf{w}}_k=0$，以及${\bf{g}}^H_k{\bf{w}}_c=0$和${\bf{g}}^H_k{\bf{w}}_c=\left| {\bf{g}}_k\right|$是矛盾的，因此RSMA中不可能完全消除所有干扰。而本文中处理方式是优先满足$\gamma_c^k$和$\gamma_p^k$分子部分两向量平行，则为$ {\bf{g}}^H_k{\bf{w}}_c=\left| {\bf{g}}_k\right|, {\bf{g}}^H_k{\bf{w}}_k=\left| {\bf{g}}_k\right|$，然后再尽可能消除干扰$ {\bf{g}}^H_k{\bf{w}}_c=\left| {\bf{g}}_k\right|, {\bf{g}}^H_k{\bf{w}}_j=0, \forall j \ne k$. 接下来先求解wk，和SDMA中求解wk的方式一样，先将所有wk合成一个矩阵${\bf{W}} = \left[ {{{\bf{w}}_1},{{\bf{w}}_2}, \cdots ,{{\bf{w}}_K}} \right] \in {C^{Nt \times K}}$，然后利用上面SDMA推导出的结果可以得到

$$
{\bf{W}} = {\bf{G}}{({{\bf{G}}^H}{\bf{G}})^{ - 1}}diag\left( {\left[ {\left| {{{\bf{g}}_1}} \right|,\left| {{{\bf{g}}_2}} \right|, \cdots ,\left| {{{\bf{g}}_K}} \right|} \right]} \right).
$$

然后求解wc，由于需满足$ {\bf{g}}^H_k{\bf{w}}_c=\left| {\bf{g}}_k\right|$，很自然地，当$ {\bf{w}}_c=\sum {\bf{w}}_k$时不仅能满足这个等式，而且还有利于每个用户解码公有信息。至此，wc和wk就都能被求出来了。$\gamma_c^k$和$\gamma_p^k$可以被简化为
$$
\begin{aligned}
\gamma _c^k &= \frac{{{\alpha _c}\rho {\beta _k}{{\left| {{{\bf{g}}_k}} \right|}^2}}}{{{{\alpha _k}\rho {\beta _k}{{\left| {{{\bf{g}}_k}} \right|}^2}}  + 1}},
\gamma _p^k &= \frac{{{\alpha _k}\rho {\beta _k}{{\left| {{\bf{g}}_k} \right|}^2}}}{{\varsigma {\alpha _c}\rho {\beta _k}{{\left| {{\bf{g}}_k} \right|}^2} + 1}}.
\end{aligned}
$$

> 文中仿真结果部分提到了两用户场景中，NOMA和RSMA我之前没注意到的差别，RSMA两个用户都需要进行SIC，而NOMA只需要强用户进行SIC就行了。当考虑imperfect CSI时，RSMA就会发生两次imperfect SIC，而NOMA只发生一次。
{: .prompt-warning }

### 3. 结论部分
- In two-user scenarios, RSMA performance is highly dependent on the common PA coefficient, and there exists a region where NOMA outperforms RSMA in OP.
- In multi-user scenarios, RSMA achieves better OP than NOMA when imperfect SIC with 10% residual interference is present.
- For throughput performance, RSMA outperforms both OMA and NOMA in most cases, regardless of SIC imperfections.
RSMA achieves a significant system throughput gain due to the additional common message component.

- Adaptive rate-splitting, user clustering, and antenna selection are effective in large-scale RSMA deployments to balance spatial multiplexing gain, diversity gain, and reduce complexity and power consumption.

