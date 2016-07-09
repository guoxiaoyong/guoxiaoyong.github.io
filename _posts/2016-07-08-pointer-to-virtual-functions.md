---
layout: post
title: "Pointer to Virtual Functions"
date: 2016-07-08 17:26:00 +0800
categories: C++
---

**Xiaoyong Guo**

I have notice that `printf` a pointer to 
a virtual function of a class output a `1`,
not an address, something like `0x400606`.

To dig deep into this, 
I wrote following class;

{% highlight c++ %}
struct A {

    virtual int fun(int);
    virtual int gun(int);
    virtual int hun(int);
};

int A::fun(int a) {

    return a+1;
}


int A::gun(int a) {

    return a+10;
}


int A::hun(int a) {

    return a+100;
}
{% endhighlight %}

{% highlight c++ %}

int main(void) {

    int (A::*p1)(int);
    int (A::*p2)(int);
    int (A::*p3)(int);

    p1 = &A::fun;
    p2 = &A::gun;
    p3 = &A::hun;

    return 0;
}

{% endhighlight %}


pointer to function is defined as:

typedef int (*pFun)(int, int);

  
  class A;
      
      typedef int (A::*PtrMemberFun)(int, int);


      How


g++ -S -m32 -O0 -masm=intel aa.cc



