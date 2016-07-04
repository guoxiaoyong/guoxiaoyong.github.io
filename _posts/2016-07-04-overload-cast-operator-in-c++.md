---
layout: post
title: "Overload casting operator in C++"
date: 2016-07-04 21:08:00 +0800
categories: C++
---

C++ prohibits overloading functions and class member functions by their return values. Some arguments for this design choice can be found [here](https://www.quora.com/Why-overloading-by-the-return-value-of-the-function-isnt-possible-in-C++). In summary, it is often not possible to deduce the types of the function's return values in the calling context, and thus can not resolve the overloaded functions.  

By overloading casting operator, we can achieve a similar effect. For example, we need three overloaded functions called div, div accepts 2 integers as input parameters, the output of div can be double, int or a pair of int. You can use it like this

{% highlight c++ %}
double a = div(10, 3); // a = 3.33333
int b = div(10,3); // b = 3
std::pair<int, int> c = div(10,3);  // c = (3, 1), the second number is remainder.
{% endhighlight %}

Of course you cannot do it using overloading.

{% highlight c++%}
#include <iostream>

using namespace std;

class DivResult {

private:

    int m;
    int n;

public:

    DivResult(int m, int n):m(m),n(n) {}

    // overload casting operators
    // Casting operators do not have a return type. 
    // C++ assumes you will be returning the correct type.
    operator double() const {

        return (double)m / (double)n;
    }

    operator int() const {

        return m/n;
    }

    operator std::pair<int,int> () const {

        return std::make_pair(m/n, m%n);
    }

};

DivResult div(int m, int n) {

    return DivResult(m, n);
}

int main(void) {

    double a = div(10, 3);
    int b = div(10, 3);
    pair<int, int> c = div(10, 3);

    cout << "a = " << a << endl;
    cout << "b = " << b << endl;
    cout << "c = (" << c.first << "," << c.second << ")" << endl;

    return 0;
}

{% endhighlight %}


## References
[Overloading Typecasts](http://www.learncpp.com/cpp-tutorial/910-overloading-typecasts/)


