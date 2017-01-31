title: Pointer to Class Data Member in C++
date: 2016-07-07 17:47:00 +0800
author: Xiaoyong Guo

Today I was reading this 
[help pages of boost MultiIndex container](http://www.boost.org/doc/libs/1_61_0/libs/multi_index/doc/tutorial/basics.html)
and encountered some C++ code that looks quite wired to me at the first glance.

```c++
typedef multi_index_container<
  employee,
  indexed_by<
    ordered_unique<identity<employee> >,
    ordered_non_unique<tag<name>,member<employee,std::string,&employee::name> >
  >
> employee_set;
```

What is the meaning of `&employee::name`? 
With some confusion, I wrote down the following code snippet,
and compiled it:

```c++
struct A {
    int a;
    int b;
};

typedef int A::*PtrToMember;

int main(void) {

    PtrToMember p1 = &A::a;
    PtrToMember p2 = &A::b;

    return 0;
}
```

It compiles smoothly. Yes this is accepted in C++!

We can get the address of an instance of a class 
and the addresses of the public data members of this instance, 
because it is in memory, it must be stored somewhere, and it must have an address!
But what does it mean when you write `&ClassName::DataMember`, 
there is no such thing exist in memory!

To understand its real meaning, I compiled the above C++ code into x86 assembly:

```
g++ -S -O0 -m32 dm.cc
```

I didn't compile the code into x86_64 assembly, 
I have a 64-bit Linux system installed actually, 
but x86_64 has too many registers, 
and its calling convention seems quite complicated to me.

I did some cleanup to the generated assembly code, 
and translated it into [nasm](http://www.nasm.us/) syntax, 
since jekyll's highlight engine does not recognize AT&T syntax.
I also added comment to each instruction.


```nasm
main:
    ; save old value of stack base register
    push ebp 

    ; update stack base register 
    mov ebp, esp

    ; make room (16 bytes) for variables p1 and p2
    ; p1 and p2 only takes 8 bytes
    ; 16 is for alignment requirement
    sub esp, 16

    ; p1 = &A::a;
    mov dword [ebp-4], 0 

    ; p2 = &A::b;
    mov dword [ebp-8], 4

    ; set value to be returned
    mov eax, 0

    ; recover stack frame of the calling procedure
    leave

    ; return
    ret
```


From the above assembly code, we can clearly see 
that what actually store in variables `p1` and `p2` 
are **offsets** of the data members of class `A`.
So if we have an instance of `A`, we can use `p1`
and `p2` in the following way:

```c++
A obj;
obj.*p1 = 10; // equivalent to obj.a = 10;
obj.*p2 = 20; // equivalent to obj.b = 20;
```

In C, there is a technique to do the similar thing.
If you have even read Linux kernel code, 
you may encounter the macro `container_of` quite often.
`container_of` is used to find the address of a `struct` 
if the address of its data member is known.
`container_of` is implemented using another 
[macro `offsetof`](https://en.wikipedia.org/wiki/Offsetof),
which is defined as:

```c++
#define offsetof(type, member) ((long) &((type *)0)->member)
```

Once you know the offset of a data member, you can derive the
address of the data member if you know the address of its container `struct`,
or you can derive the address of the container `struct` if you know the address
of the data member.


 
