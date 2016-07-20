---
layout: post
title: "Value Category in C++11"
date: 2016-07-20 10:09:37 +0800
categories: C++
---

**Xiaoyong Guo**

In C++11, an expression has a property called **value category**.
There are 5 value categories defined: lvalue, xvalue, rvalue, glvalue, prvalue.


1. **lvalue**: 
2. **xvalue**: expiring value
3. **rvalue**:
4. **glvalue**: generalized lvalue
5. **prvalue**: pure rvalue

An expression belongs to one of the three fundamental categories: lvalue, xvalue or rvalue.


## References

1. [What are rvalues lvalues xvalues glvalues and prvalues](http://stackoverflow.com/questions/3601602/what-are-rvalues-lvalues-xvalues-glvalues-and-prvalues)
2. [Value category of C++11](http://en.cppreference.com/w/cpp/language/value_category)
3. [A Taxonomy of Expression Value Categories](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2010/n3055.pdf)


