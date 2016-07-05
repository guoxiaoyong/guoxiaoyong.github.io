---
layout: post
title: "Move semantics in C++11"
date: 2016-07-03 18:17:11 +0800
categories: C++
---

**Xiaoyong Guo**

Move semantics in C++11 is introduced to reduce the overhead caused by
object copying. The semantics of move and copy in C++11 is very much
like move and copy operation on files in a filesystem.
You may already have noticed that: 
copying a file from one folder to another folder takes quite a while 
if the file is large, while moving the file from one folder to 
another folder takes almost no time, 
provide that the two folders are on the same partitioin. 
No matter how large the file is, move operation finishes immediately.
This is because in order to copying a file, 
you need to read the whole file, and then write it onto the harddisk.
The larger the file is, the longer it takes.
While to moving a file you only need to modify the metadata 
of the filesystem to indicate that the parent folder of 
the file is changed to another.

Imaging that there is a filesystem that does not provide 
any mechanism to modify its metadata to indicate the change of 
the parent folder of a file.
What you can do with this particular filesystem are 
creating a file and removing a file, 
then move operation can be done in two steps: first make a copy 
the original file in the destination folder, 
then remove the original file in the source folder.
This is obviously a bad design since it makes move operation 
unnecessarily take long time to finish.
But this is the case for C++ before the introduction 
of move semantics: in order to move an object,
you have to copy it and destroy the original one.


## Reference
[Move semantics and rvalue references in C++11](http://www.cprogramming.com/c++11/rvalue-references-and-move-semantics-in-c++11.html)


