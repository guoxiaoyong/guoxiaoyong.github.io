---
layout: post
title: "Volatile Quantifier in C/C++"
date: 2016-07-30 10:50:51 +0800
categories: C++
---

**Xiaoyong Guo**

**volatile** keyword in C and C++ is a quantifer 
to prevent unwanted optimization.
In case the compiler determines a variable cannot be
modified in some scope, then it will cache the value of
the variable in the register, and use the cached value
for subsequent uses of the variable. For example: 

{% highlight c++ %}
int a = 1;
int b;
int c;

void fun() {

    b = a; 
    c = a;
}
{% endhighlight %}

Let's compile the code with the optimization switch turned on, 

```
gcc -S a.c -O2 -m32 -masm=intel volatile.c
```

We get the following assembly code:
{% highlight nasm %}
fun:
	mov	eax, DWORD PTR a
	mov	DWORD PTR b, eax
	mov	DWORD PTR c, eax
	ret
{% endhighlight %}

In the resulting assembly code, the value of `a` is first
cached in register `eax`, then the value is moved from `eax` to 
`b` and `c` in two consecutive instructions. 
The compiler assumes that the value of `a` is not
changed because it does not see any statement in the scope that
changes the value of a. 
So compiler think the two variables `b` and `c` 
always have the same value.

But this optimization is not always what we want. For example,
the value of `a` can be modified by some hardware 
or another thread, what we want is to store the current value of `a`
in `b` and `c`.

If we turn off optimization switch, 
the resulting assembly code is:

{% highlight nasm %}
fun:
	push	ebp
	mov	ebp, esp
	mov	eax, DWORD PTR a
	mov	DWORD PTR b, eax
	mov	eax, DWORD PTR a
	mov	DWORD PTR c, eax
	nop
	pop	ebp
	ret
{% endhighlight %}

We can see to assign the value of `a` to `b`, 
the value of `a` is first fetched and stored in register `eax`, 
then moved from `eax` to `b`. 
This process is repeat for the assignment of `c`,
the **fetching** step is not omited. 

What if we want the compiler to do optimization for the other
part of the code, but stop this wrong value caching optimization
for `a`? 
We can simply add a **volatile** quantifier to `a`. 

Use the command

```
gcc -S a.c -O2 -m32 -masm=intel volatile.c
```
to compile the following code:


{% highlight c++ %}
volatile int a = 1;
int b;
int c;

void fun() {

    b = a;
    c = a;
}
{% endhighlight %}

We get this result:

{% highlight nasm %}
fun:
	mov	eax, DWORD PTR a
	mov	DWORD PTR b, eax
	mov	eax, DWORD PTR a
	mov	DWORD PTR c, eax
	ret
{% endhighlight %}

This result shows that the compiler did optimization to 
stack management for the simple function `fun`,
but abandoned the value caching optimization
which we do not want.

In C++, we can achieve the same effect by declaring variable `a`
as an atomic object:

{% highlight c++ %}
std::atomic<int> a;
{% endhighlight %}

C++11 discourages the use of `volatile` for inter-thread communication.
Use of atomic object is recommended.

> The volatile keyword in C++11 ISO Standard code is to be used only for hardware access; do not use it for inter-thread communication. For inter-thread communication, use mechanisms such as std::atomic<T> from the C++ Standard Template Library.

The following code is an example of using `int`, `volatile int`
and `std:atomic<int>` to do inter-thread communication. 
If you compile the code (using the provided Makefile) 
and run it, you will find
that it will not do what you expected in `MODE 1`. 

I knew the keyword `volatile` for sometime 
and probably saw it in some other people's code. 
I thought I know its meaning.
But I didn't really understand its usefulness until
one day I experienced a very strange software bug. 
This bug in its simplest from, is the same as `MODE 1`
of the following code.


{% highlight c++ %}
#include <iostream>
#include <thread>
#include <atomic>

using namespace std;

#if  MODE==1

// no protection against optimization
int quit(0);

#elif MODE==2

// not recommended by C++11
volatile int quit(0);

#else

// recommended by C++11
std::atomic<int> quit(0);

#endif

void loop() {

    while (true) {

        if (quit) break;
    }
}

void control() {

    char tmp;
    std::cin >> tmp;
    quit = 1;
}

int main(void) {

    thread t1(loop);
    thread t2(control);
    t1.join();
    t2.join();
    return 0;
}

{% endhighlight %}

{% highlight makefile %}

ifeq ($M,1)
mode := -DMODE=1
endif

ifeq ($M,2)
mode := -DMODE=2
endif

ifeq ($M,3)
mode := -DMODE=3
endif

CXXFLAGS := -O4 -std=c++11 $(mode)
LDLIBS := -lpthread

all: main
	
{% endhighlight %}


## References
1. [Understanding “volatile” qualifier in C](http://www.geeksforgeeks.org/understanding-volatile-qualifier-in-c/)
2. [volatile (computer programming)](https://en.wikipedia.org/wiki/Volatile_%28computer_programming%29)
