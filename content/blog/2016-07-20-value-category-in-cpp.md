title: Value Category in C++11
date: 2016-07-20 10:09:37 +0800
author: Xiaoyong Guo

In C++11, an expression has a property called **value category**.
There are 5 value categories defined: 

1. **lvalue**: left value
2. **xvalue**: expiring value
3. **rvalue**: right value
4. **glvalue**: generalized lvalue
5. **prvalue**: pure rvalue

The following figure shows the taxonomy of the expression categorization.

![value category taxonomy](/images/value_category.png)

An expression belongs to one of the three fundamental categories: lvalue, xvalue or rvalue.

xvalues are created by three kinds of expressions:

1. Function calls (explicit or implicit) that return rvalue references to objects;
2. Casts to rvalue references to objects;
3. Class member access and pointer-to-data-member dereference expressions where the object expression is an xvalue.

## References

1. [What are rvalues lvalues xvalues glvalues and prvalues](http://stackoverflow.com/questions/3601602/what-are-rvalues-lvalues-xvalues-glvalues-and-prvalues)
2. [Value category of C++11](http://en.cppreference.com/w/cpp/language/value_category)
3. [A Taxonomy of Expression Value Categories](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2010/n3055.pdf)


