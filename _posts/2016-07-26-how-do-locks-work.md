---
layout: post
title: "How do Locks Work?"
date: 2016-07-26 11:16:15 +0800
categories: C++
---

**Xiaoyong Guo**


On x86/x86\_64 platforms (>= i486), 
a CPU core can assert a LOCK signal so that only this core 
can modify the content of a particular memory address.
There are a few instructions that can be prefixed with `lock`.
One such instructions is `cmpxchg`, which is usually used to implement locks
such as mutex.

`cmpxchg` stands for **compare and exchange**. 
It has two operands, the first operand can be a register or memory address,
the second operand is register. What `cmpxchg` actually does is shown in the following code:

{% highlight c %}
// cmpxchg r/m (v), r (b)
if (eax == v) {

    zf = 1;
    v = b;

} else {

    zf = 0;
    eax = v;
}
{% endhighlight c%}

**compare and exchange** is also called **compare and swap** in some literatures.
It is a very important technique to do synchronization between threads.
The semantics of **compare and exchange** is: I think `V` should be `A`, if it is, 
then set `V` to `B`, otherwise, return the value of `V`. If written in C, it should
look like this:

{% highlight c %}
int compare_and_swap (int* m, int expected, int val) {

    int oval = *m;

    if (*m == expected) {

        *m = val;
    }

    return oval;
}
{% endhighlight %}

In C++11, `atomic_compare_exchange_weak` and `atomic_compare_exchange_strong`
does the same thing. Actually, they are wrappers of `lock cmpxchg` on x86/x86_64 platform.

{% highlight c++ %}
#include <atomic>

using namespace std;

struct SpinLock {

    atomic<int> a(0);
    int expected = 0;
    int val = 1;
};

void SpinLock_lock(SpinLock* sl) {

    while ( atomic_compare_exchange_strong(&a, &t, val) );
}


void SpinLock_unlock(SpinLock* sl) {

    while ( atomic_compare_exchange_strong(&a, &val, t) );
}


int main(void) {

    return 0;

}

{% endhighlight %}
