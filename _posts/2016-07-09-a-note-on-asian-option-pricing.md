---
layout: post
title: "A Note on Asian Option Pricing"
date: 2016-07-09 13:17:01 +0800
categories: C++
---

**Xiaoyong Guo**

Today I did a few google search, and managed to make [MathJax](https://www.mathjax.org/) 
work with [jekyll](http://jekyllrb.com/), 
the setup process is [very easy](http://jekyllrb.com/docs/extras/).
This post is about [Asian option pricing](https://en.wikipedia.org/wiki/Asian_option).
It is also my first experiment with writing LaTeX equations on a webpage using MathJax. 


![asian option time line](/image/asian_option_timeline.svg)

Let's say that we already have a library routine 
that calculates the price of an asian call option 
for the case when the valuation date is the same as the beginning of average period,
then **how to calculate the option price using this routine 
if these two dates are different?**

We know that the price of an Asian call option at time $t$ is

$$
\begin{equation}
\label{eq:callpayoffx}
C(t) = e^{-r(T-t)} E\left[ \left(\bar{S}-K\right)^+ \right]
\end{equation}
$$

or

$$
\begin{equation}
\label{eq:callpayoff}
 e^{r(T-t)} C(t) = E\left[ \left(\bar{S}-K\right)^+ \right]
\end{equation}
$$


where $\bar{S}$  is the average price over the period $[0, T]$.
If $\bar{S}$ is a continuous/discrete arithmetic average, then $\bar{S}$ can be written as:

$$
\begin{equation}
\label{eq:avgeqn}
\bar{S} = \frac{ t \bar{S}_0 + (T-t)\bar{S}_1}{T}
\end{equation}
$$

where $\bar{S}_0$ is the average price over time $[0, t]$, and
$\bar{S}_1$ is the average price over time $[t, T]$.

Substitute Eq. \eqref{eq:avgeqn} into Eq. \eqref{eq:callpayoff}, 
we get

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

We can see that in both cases, 
our problem can be reduced to 
the calculation of asian option price
using the said library routine.





