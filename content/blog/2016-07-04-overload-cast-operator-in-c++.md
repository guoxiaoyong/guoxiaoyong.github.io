title: Overload Casting Operator in C++
date: 2016-07-04 21:08:00 +0800
author: Xiaoyong Guo

C++ prohibits overloading functions and class member functions by their return values. Some arguments for this design choice can be found [here](https://www.quora.com/Why-overloading-by-the-return-value-of-the-function-isnt-possible-in-C++). In summary, it is often not possible to deduce the types of the function's return values in the calling context, and thus can not resolve the correct overloaded function.  

By overloading casting operator, we can achieve a similar effect. For example, we need three overloaded functions called `div`, `div` accepts 2 integers as input parameters, the return value of `div` can be `double`, `int` or a pair of int `std::pair<int, int>`. We can use it like this:

```c++
double a = div(10, 3); // a = 3.33333
int b = div(10,3); // b = 3

// c = (3, 1), the second number is remainder.
std::pair<int, int> c = div(10,3);  
```

Of course you cannot simply overload `div` like this:

```c++
#include <map>

double div(int m, int n) {

    return (double)m / (double)n;
}

int div(int m, int n) {

    return m/n;
}

std::pair<int, int> div(int m, int n) {

    return std::make_pair(m/n, m%n);
```

You'll get a compiling error complaining ambiguous function declaration.
The tick is to let `div` return a class type, 
which we named `DivResult`, and overload casting operator for class `DivResult`.  

```c++
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
```


## References
[Overloading Typecasts](http://www.learncpp.com/cpp-tutorial/910-overloading-typecasts/)


