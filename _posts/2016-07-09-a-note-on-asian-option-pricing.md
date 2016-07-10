---
layout: post
title: "A Note on Asian Option Pricing"
date: 2016-07-09 13:17:01 +0800
categories: C++
---

**Xiaoyong Guo**

Making [MathJax](https://www.mathjax.org/) 
work with [jekyll](http://jekyllrb.com/) 
seems [very easy](http://jekyllrb.com/docs/extras/).

This post is about [Asian option pricing](https://en.wikipedia.org/wiki/Asian_option).


We know that a Asian call option

$$
\begin{equation}
\label{eq:callpayoff}
C(t) = e^{-r(T-t)} E\left[ \left(\bar{S}-K\right)^+ \right]
\end{equation}
$$

where $\bar{S}$  is the average price over the period $[0, T]$.
Since $\bar{S}$ can be written as:

$$
\begin{equation}
\label{eq:avgeqn}
\bar{S} = \frac{ t \bar{S}_0 + (T-t)\bar{S}_1}{T}
\end{equation}
$$

Substitute Eq. (\ref{eq:avgeqn}) into Eq. (\ref{eq:callpayoff}), we get

$$
\begin{eqnarray}
E\left[ \left(\bar{S}-K\right)^+ \right]
& = & E\left[ \left(\frac{t\bar{S}_0+(T-t)\bar{S}_1}{T} - K \right)^+ \right] \\
& = & E\left[ \left( \frac{T-t}{T}\bar{S}_1 - \left(K - \frac{t}{T}\bar{S}_0\right) \right)^+ \right]
\end{eqnarray}
$$

In case $K - \frac{t}{T}\bar{S}_0 > 0$,  

$$
\begin{equation}
\label{eq:greaterthanzero}
E\left[ \left(\bar{S}-K\right)^+ \right] = \frac{T-t}{T} E\left[ \bar{S}_1 - \left(\frac{T}{T-t}K - \frac{t}{T-t}\bar{S}_0 \right)^+ \right]
\end{equation}
$$



In case $K - \frac{t}{T}\bar{S}_0 \le 0$,  

$$
\begin{equation}
\label{eq:lessthanzero}
E\left[ \left(\bar{S}-K\right)^+ \right] = \frac{T-t}{T} E\left[ \bar{S}_1 \right] - K + \frac{t}{T}\bar{S}_0 
\end{equation}
$$





