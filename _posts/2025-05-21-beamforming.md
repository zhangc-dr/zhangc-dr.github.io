---
title: 如何理解基站发送的信号可以被建模为x=Σpksk
description: 本博客解释了MIMO系统中$x=Σp_{k}s_{k}$这种建模方式与不同beamforming结构（analog, digital, hybrid）的关系，以及为什么该模型主要适用于digital beamformer。
author: Chen Zhang
date: 2025-05-21 00:00:00 +0800
categories: [wireless communications]
tags: [beamformer]
pin: true
math: true
mermaid: true
---

**视频：**
{% include embed/youtube.html id='iMIqEpzxN9Y' %}

**个人理解：**
- 要理解为什么这么建模，我觉得应该先了解被建模的对象在real world是什么样的。以我当前认知我认为对于MIMO系统中天线首先天线数肯定是多根的，然后每根天线还接了一个amplifier和一个移相器，这样的结构就能实现beamforming了，往指定方向聚集波束。但看了博客发现这其实是analog beamformer的结构，而这个建模根本没办法通过analog beamformer来实现（参考博客[What is the difference between analog, digital and hybrid beamforming?](https://wirelesspi.com/what-is-the-difference-between-analog-digital-and-hybrid-beamforming/)中这么一句话：it is difficult to support multiple streams for multiuser MIMO. In general, a phase shifted version of the same signal is sent from all the antennas into a particular direction）。
- 那么这个模型是根据什么结构建模的呢？有analog beamformer肯定就还有digital beamformer，这个模型也正是根据digital beamformer的结构构建出来的。digital beamformer不再像analog beamformer那样需要使用amplifier和移相器来实现beamforming了，而是直接在数字处理单元（我也不知道叫啥，姑且这么叫）中进行编码，然后由DAC转换成analog signal，然后传输到天线发送出去。
