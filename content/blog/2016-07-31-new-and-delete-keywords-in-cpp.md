title: A Few Notes on new and delete Keywords in C++
date: 2016-07-31 09:12:56 +0800
author: Xiaoyong Guo

**new** operator in C++ is used to create a new object in the heap.
There are two steps in the process of creating 
a new object using **new** operator: 

1. allocate memory for the object using the function **operator new**. 
2. initialize the object properties by invoking the class costructor. 

Note that C++ jargon makes a distinction between **new** operator 
and operator **new**. **new** operator is an operator, 
and operator **new** is a function that can be overloaded, 
and it is part of the **new** operation..

**operator new** has a few overloaded forms. In C++11, there are three
overloaded **operator new** functions. 

```c++
// throwing 
void* operator new (std::size_t size);

// nothrow 
void* operator new (std::size_t size, 
                    const std::nothrow_t& nothrow_value) noexcept;

// placement 
void* operator new (std::size_t size, void* ptr) noexcept;
```

Usually **operator new** functions are invoked by **new** operator.
In the following example, we use **new** operator to invoking the three
difference forms of **operator new** functions.

```c++
struct A {

    int data[100];

    A() {

       data[0]= 123;
    }

    ~A() {
       data[0] = 321;
    }
};

#include <new>
int main(int argc, char* argv[]) {

    char m[1024];

    // added as a delimiter in the resulting asm
    asm("nop"); 
    A* p1 = new A();

    asm("nop");
    A* p2 = new(std::nothrow) A();

    asm("nop");
    A* p3 = new((void*)m) A();

    asm("nop");
    delete p1;

    asm("nop");
    delete p2;

    asm("nop");
    p3->~A();

    return 0;
}
```

Makefile to compile the above code is:

```Makefile
new.s: new.cc
	g++ -O0 -S -m32 -masm=intel -o - $^ | grep -v cfi | c++filt > $@
```

The resulting asm code is

```nasm
	.file	"new.cc"
	.intel_syntax noprefix
	.section	.text._ZN1AC2Ev,"axG",@progbits,A::A(),comdat
	.align 2
	.weak	A::A()
	.type	A::A(), @function
A::A():
.LFB1:
	push	ebp
	mov	ebp, esp
	mov	eax, DWORD PTR [ebp+8]
	mov	DWORD PTR [eax], 123
	nop
	pop	ebp
	ret
.LFE1:
	.size	A::A(), .-A::A()
	.weak	A::A()
	.set	A::A(),A::A()
	.section	.text._ZN1AD2Ev,"axG",@progbits,A::~A(),comdat
	.align 2
	.weak	A::~A()
	.type	A::~A(), @function
A::~A():
.LFB4:
	push	ebp
	mov	ebp, esp
	mov	eax, DWORD PTR [ebp+8]
	mov	DWORD PTR [eax], 321
	nop
	pop	ebp
	ret
.LFE4:
	.size	A::~A(), .-A::~A()
	.weak	A::~A()
	.set	A::~A(),A::~A()
	.section	.text._ZnwjPv,"axG",@progbits,operator new(unsigned int, void*),comdat
	.weak	operator new(unsigned int, void*)
	.type	operator new(unsigned int, void*), @function
operator new(unsigned int, void*):
.LFB15:
	push	ebp
	mov	ebp, esp
	mov	eax, DWORD PTR [ebp+12]
	pop	ebp
	ret
.LFE15:
	.size	operator new(unsigned int, void*), .-operator new(unsigned int, void*)
	.text
	.globl	main
	.type	main, @function
main:
.LFB19:
	lea	ecx, [esp+4]
	and	esp, -16
	push	DWORD PTR [ecx-4]
	push	ebp
	mov	ebp, esp
	push	ebx
	push	ecx
	sub	esp, 1040
#APP
# 20 "new.cc" 1
	nop
# 0 "" 2
#NO_APP
	sub	esp, 12
	push	400
	call	operator new(unsigned int)
	add	esp, 16
	mov	ebx, eax
	sub	esp, 12
	push	ebx
	call	A::A()
	add	esp, 16
	mov	DWORD PTR [ebp-12], ebx
#APP
# 23 "new.cc" 1
	nop
# 0 "" 2
#NO_APP
	sub	esp, 8
	push	OFFSET FLAT:std::nothrow
	push	400
	call	operator new(unsigned int, std::nothrow_t const&)
	add	esp, 16
	mov	ebx, eax
	test	ebx, ebx
	je	.L6
	sub	esp, 12
	push	ebx
	call	A::A()
	add	esp, 16
	mov	eax, ebx
	jmp	.L7
.L6:
	mov	eax, ebx
.L7:
	mov	DWORD PTR [ebp-16], eax
#APP
# 26 "new.cc" 1
	nop
# 0 "" 2
#NO_APP
	lea	eax, [ebp-1044]
	sub	esp, 8
	push	eax
	push	400
	call	operator new(unsigned int, void*)
	add	esp, 16
	mov	ebx, eax
	test	ebx, ebx
	je	.L8
	sub	esp, 12
	push	ebx
	call	A::A()
	add	esp, 16
	mov	eax, ebx
	jmp	.L9
.L8:
	mov	eax, ebx
.L9:
	mov	DWORD PTR [ebp-20], eax
#APP
# 29 "new.cc" 1
	nop
# 0 "" 2
#NO_APP
	mov	ebx, DWORD PTR [ebp-12]
	test	ebx, ebx
	je	.L10
	sub	esp, 12
	push	ebx
	call	A::~A()
	add	esp, 16
	sub	esp, 12
	push	ebx
	call	operator delete(void*)
	add	esp, 16
.L10:
#APP
# 32 "new.cc" 1
	nop
# 0 "" 2
#NO_APP
	mov	ebx, DWORD PTR [ebp-16]
	test	ebx, ebx
	je	.L11
	sub	esp, 12
	push	ebx
	call	A::~A()
	add	esp, 16
	sub	esp, 12
	push	ebx
	call	operator delete(void*)
	add	esp, 16
.L11:
#APP
# 35 "new.cc" 1
	nop
# 0 "" 2
#NO_APP
	sub	esp, 12
	push	DWORD PTR [ebp-20]
	call	A::~A()
	add	esp, 16
	mov	eax, 0
	lea	esp, [ebp-8]
	pop	ecx
	pop	ebx
	pop	ebp
	lea	esp, [ecx-4]
	ret
.LFE19:
	.size	main, .-main
	.ident	"GCC: (GNU) 5.3.1 20160406 (Red Hat 5.3.1-6)"
	.section	.note.GNU-stack,"",@progbits
```

If the object is no longer needed, you have to use
**delete** operator use do the clean-up and return the memory. 

From the above assembly code, we see that **delete operator**
checks the value of the pointer, if it is 0, then delete does nothing.
other wise it will invoke class destructor, then **operator delete**
is called to return the memory. In case object is created using 
replacement form of new, then we cannot delete the object, that will
cause a segment fault. We have to call class destructor explicitly.

We can explicitly call **operator new** functions.

To create an array of objects, you have to use **new[]** operator. 
Objects created using **new[]** operator have to be freed 
using **delete[]** operator.

Operator **new** can be overloaded.


## References
1. [My Rant on C++'s operator new](http://www.scs.stanford.edu/~dm/home/papers/c++-new.html)
2. [The many faces of operator new in C++](http://eli.thegreenplace.net/2011/02/17/the-many-faces-of-operator-new-in-c)
