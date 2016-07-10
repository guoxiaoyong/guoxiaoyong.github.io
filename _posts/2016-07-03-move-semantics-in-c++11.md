---
layout: post
title: "Move Semantics in C++11: A Metaphoric Explanation"
date: 2016-07-03 18:17:11 +0800
categories: C++
---

**Xiaoyong Guo**

Move semantics in C++11 is introduced to 
reduce the overhead caused by object copying. 

The semantics of move and copy in C++11 is very much
like move and copy operation on files in a filesystem.
You may already have noticed that: 
copying a file from one folder to another folder takes quite a while 
if the file is large, while moving the file from one folder to 
another folder takes almost no time, 
providing that the two folders are on the same partition. 
No matter how large the file is, move operation finishes immediately.
This is because in order to copying a file, 
you need to read the whole file, and then write it onto the harddisk.
The larger the file is, the longer it takes.
While to move a file you only need to modify the metadata 
of the filesystem to indicate that the parent folder of 
the file is changed to another.

Imaging that there is a filesystem that does not provide 
any mechanism to modify its metadata to indicate the change of 
the parent folder of a file.
What you can do with this particular filesystem are 
creating a file and removing a file, 
then move operation can be done in two steps: first make a copy of 
the original file in the destination folder, 
then remove the original file in the source folder.
This is obviously a bad design since it makes move operation 
unnecessarily take long time to finish.
But this is the case for C++ before the introduction 
of move semantics: in order to move an object (usually a temporary object),
you have to copy it and then destroy the original one. 
This is an inefficient way of transfering resources from one object to another. 

C++11 added a new language construct 
called rvalue reference (`type &&`) to allow "move semantics".
rvalue reference is supposed to bind to a temporary object, i.e., an rvalue, 
then you can modify the temporary object via the rvalue reference.
rvalue reference is useful in defining the two special member functions introduced in C++11: 
the **move constructor** and the **move assignment operator**. These two special member functions
are supposed to implement the move semantics. 
Move constructor and move assignment operator should behave in a way like this: 
when invoked, the control of resources of the input object is transfered to **this object**, 
after that the input object is invalidated.

Since rvalue reference can only bind to a temporary object, 
so we can only move resources from an temporary object to another non-temporary object.
What if we want to move resources from a non-temporary object to another  non-temporary object?
This is the case where `std::move` comes into play. `std::move` cast a lvalue to an rvalue reference,
so move constructor or move assignment operator can be called to complete the resouce move operation.



## References
1. [Move semantics and rvalue references in C++11](http://www.cprogramming.com/c++11/rvalue-references-and-move-semantics-in-c++11.html)
2. [When should I use std::move in C++11](https://www.quora.com/When-should-I-use-std-move-in-C++11)
3. [Introducing the move constructor and move assignment operator](http://blog.smartbear.com/c-plus-plus/c11-tutorial-introducing-the-move-constructor-and-the-move-assignment-operator/)



