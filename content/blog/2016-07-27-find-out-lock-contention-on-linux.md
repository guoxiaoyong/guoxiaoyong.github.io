title: Find out Lock Contention on Linux
date: 2016-07-27 11:54:03 +0800
author: Xiaoyong Guo

When testing a multi-threaded program, 
which use `lock` to protect its critical section,
you may want to know how often these threads are
contenting to gain the ownership of the lock.

A simple method is to use `strace`, 

```c++
strace -f program
```

`strace` will list all the system calls.
Note that you must add the switch `-f` 
so that `strace` will also trace threads and child processes,
otherwise `strace` list system calls made by the main thread only.
Since pthread mutex is build on top of `futex`, by check the number of
`futex` system calls in the list, 
you can get the idea of whether the contention for lock is intense or not.
You can also list the system calls made by each thread 
in different files using `-o` and `-ff` switch:

```c++
strace -o result -ff program
```

Context switches of a running program 
can be find out from the file `/proc/$pid/status`



