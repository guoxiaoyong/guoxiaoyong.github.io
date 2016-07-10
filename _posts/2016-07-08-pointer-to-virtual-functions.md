---
layout: post
title: "An Investigation On Pointers to Virtual Functions in C++"
date: 2016-07-08 17:26:00 +0800
categories: C++
---

**Xiaoyong Guo**


I have noticed that if you print out 
the value of a pointer to a virtual function 
of a class using `printf("%p\n", ptr)`, 
the result is a `1`.
In contrast, 
the value of a pointer to a regular function 
or member function is something like `0x400606`.

In order to develop a better understanding of this phenomenon,
I designed a very simple class `A` as follows:

{% highlight c++ linenos %}
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

In the following `main` function, 
the addresses of virtual functions of class `A`
are assigned to variables 
`p1`, `p2` and `p3`.
Then an instance `a` of class `A` is constructed,
a pointer `b` points to the variable `a` is defined.
After that, I use three different forms 
to call virtual functions. 

{% highlight c++ linenos %}

int main(void) {

    int (A::*p1)(int);
    int (A::*p2)(int);
    int (A::*p3)(int);

    p1 = &A::fun;
    p2 = &A::gun;
    p3 = &A::hun;

    A a;
    A* b = &a;

    a.fun(22);
    b->gun(23);
    (a.*p3)(24);

    return 0;
}
{% endhighlight %}

Then I type the following command to compile the C++ code
into x86 assembly code
(I just learned how to make g++ 
generate assembly code with intel syntax):

{% highlight bash %}
g++ -S -m32 -O0 -masm=intel test.cc
# remove some irrelavant directives and demangle C++ symbols.
cat test.s | grep -v cfi | grep -v .LF | c++filt > result.s
{% endhighlight %}

The following is 
the resulting x86 assembly code 
(different versions of g++ seems to generate
somewhat different assembly code, my g++ version is v5.3.1): 

{% highlight nasm linenos %}
    .file   "test.cc"
    .intel_syntax noprefix
    .text
    .align 2
    .globl  A::fun(int)
    .type   A::fun(int), @function
A::fun(int):
    push    ebp
    mov ebp, esp
    mov eax, DWORD PTR [ebp+12]
    add eax, 1
    pop ebp
    ret
    .size   A::fun(int), .-A::fun(int)
    .align 2
    .globl  A::gun(int)
    .type   A::gun(int), @function
A::gun(int):
    push    ebp
    mov ebp, esp
    mov eax, DWORD PTR [ebp+12]
    add eax, 10
    pop ebp
    ret
    .size   A::gun(int), .-A::gun(int)
    .align 2
    .globl  A::hun(int)
    .type   A::hun(int), @function
A::hun(int):
    push    ebp
    mov ebp, esp
    mov eax, DWORD PTR [ebp+12]
    add eax, 100
    pop ebp
    ret
    .size   A::hun(int), .-A::hun(int)
    .section    .text._ZN1AC2Ev,"axG",@progbits,A::A(),comdat
    .align 2
    .weak   A::A()
    .type   A::A(), @function
A::A():
    push    ebp
    mov ebp, esp
    mov edx, OFFSET FLAT:vtable for A+8
    mov eax, DWORD PTR [ebp+8]
    mov DWORD PTR [eax], edx
    nop
    pop ebp
    ret
    .size   A::A(), .-A::A()
    .weak   A::A()
    .set    A::A(),A::A()
    .text
    .globl  main
    .type   main, @function
main:
    lea ecx, [esp+4]
    and esp, -16
    push    DWORD PTR [ecx-4]
    push    ebp
    mov ebp, esp
    push    edi
    push    esi
    push    ebx
    push    ecx
    sub esp, 40
    mov esi, 1
    mov edi, 0
    mov DWORD PTR [ebp-36], esi
    mov DWORD PTR [ebp-32], edi
    mov ecx, 5
    mov ebx, 0
    mov DWORD PTR [ebp-44], ecx
    mov DWORD PTR [ebp-40], ebx
    mov eax, 9
    mov edx, 0
    mov DWORD PTR [ebp-52], eax
    mov DWORD PTR [ebp-48], edx
    sub esp, 12
    lea eax, [ebp-56]
    push    eax
    call    A::A()
    add esp, 16
    lea eax, [ebp-56]
    mov DWORD PTR [ebp-28], eax
    sub esp, 8
    push    22
    lea eax, [ebp-56]
    push    eax
    call    A::fun(int)
    add esp, 16
    mov eax, DWORD PTR [ebp-28]
    mov eax, DWORD PTR [eax]
    add eax, 4
    mov eax, DWORD PTR [eax]
    sub esp, 8
    push    23
    push    DWORD PTR [ebp-28]
    call    eax
    add esp, 16
    mov eax, DWORD PTR [ebp-52]
    and eax, 1
    test    eax, eax
    jne .L9
    mov eax, DWORD PTR [ebp-52]
    jmp .L10
.L9:
    mov eax, DWORD PTR [ebp-48]
    mov edx, eax
    lea eax, [ebp-56]
    add eax, edx
    mov eax, DWORD PTR [eax]
    mov edx, DWORD PTR [ebp-52]
    sub edx, 1
    add eax, edx
    mov eax, DWORD PTR [eax]
.L10:
    mov edx, DWORD PTR [ebp-48]
    mov ecx, edx
    lea edx, [ebp-56]
    add edx, ecx
    sub esp, 8
    push    24
    push    edx
    call    eax
    add esp, 16
    mov eax, 0
    lea esp, [ebp-16]
    pop ecx
    pop ebx
    pop esi
    pop edi
    pop ebp
    lea esp, [ecx-4]
    ret
    .size   main, .-main
    .weak   vtable for A
    .section    .rodata._ZTV1A,"aG",@progbits,vtable for A,comdat
    .align 4
    .type   vtable for A, @object
    .size   vtable for A, 20
vtable for A:
    .long   0
    .long   typeinfo for A
    .long   A::fun(int)
    .long   A::gun(int)
    .long   A::hun(int)
    .weak   typeinfo for A
    .section    .rodata._ZTI1A,"aG",@progbits,typeinfo for A,comdat
    .align 4
    .type   typeinfo for A, @object
    .size   typeinfo for A, 8
typeinfo for A:
    .long   vtable for __cxxabiv1::__class_type_info+8
    .long   typeinfo name for A
    .weak   typeinfo name for A
    .section    .rodata._ZTS1A,"aG",@progbits,typeinfo name for A,comdat
    .type   typeinfo name for A, @object
    .size   typeinfo name for A, 3
typeinfo name for A:
    .string "1A"
    .ident  "GCC: (GNU) 5.3.1 20160406 (Red Hat 5.3.1-6)"
    .section    .note.GNU-stack,"",@progbits
{% endhighlight %}


Keep in mind that `long` and `pointer type` 
are 32-bit long since I choose to 
generate 32-bit assembly code.


From line 67 to line 78, 
we can see that `p1 = 1`, `p2 = 5` and `p3 = 9`.
If I choose to generate 64-bit assembly code, you'll see
that these three values are `1`, `9` and `17`.
So, it seems that the values stored in the 
pointers to virtual functions are 
**offsets of virutual functions in the vtable plus 1**. 
`vtable for A` is defined in line 142, 
where the first 8 bytes seems to be ignored when assigning
vtable address in the constructor of `A` in line 44.


Line 87-90 corresponds to the C++ code `a.fun(22)`. 
In line 90 the function address of `A::fun(int)` is called directly,
So we can conclude that there is no overhead incurred by 
calling a virtual function using the form `Object.Function`.


Line 92-99 corresponds to the C++ code `b->gun(23)`.  Line 92-95 
are the steps to get the address of the virtual 
function to be called from vtable. 
So call virtual function via a pointer to class `A`
incurs some overhead, 
4 additional instructions are needed to resolve
the address of the virtual function to be called.

Line 101-125 corresponds to the C++ code `a::*p3(24)`. 
We can see that this form of virtual function calling
is very expensive.
First you need to determine wether `p3` is a pointer
to a virtual function or a regular member function.
This is done by checking whether the value of `p3` is an odd number
or an even numer (line 102-103).
If the value is odd, then it is assumed 
that `p3` is a virtual function pointer 
(this is the reason for adding 1 to the offset).
To call the virtual function, you have to find the address of 
the function by looking up the vtable (line 108-116). 
Note that in line 114, the value of `p3` is substracted by 1
to get the offset.
If value in `p3` is an even number, 
then it is assumed that `p3` is 
a regular member function pointer. The value of `p3` is 
used as the function address to be called 
(line 105 and line 125).


## Performance Test Results

I did a simple performance benchmark.
The three function calls `a.fun(22)`, `b->fun(22)` and `a::*p1(22)` 
are iterated for `1e10` times.
The results are shown in the following table.


| Function Call | Time (seconds) |
|--------------|--------|
| `a.fun(22)`  | 84.475 |
| `b->fun(22)` | 92.959 |
| `a::*p1(22)` | 141.373 |


## Conclusions

1. Pointer to a virtual function stores a value that equals to the offset of the virtual function in vtable plus 1.
2. The calling form `Object.Function` incurs no overhead compared to calling a non-virtual function. 
3. The calling form `PtrToObject->Function` incurs a relatively small overhead. 
4. The calling form `Object.*PtrToFunction` incurs a relatively big overhead.

Remember that **item 3** and **item 4** are based on the assumption that the g++ optimization switch is off. 
C++ compiler is able to optimize the generated assembly code to reduce this function calling overhead in many cases.


