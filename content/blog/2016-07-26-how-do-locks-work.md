title: How do Locks Work?
date: 2016-07-26 11:16:15 +0800
author: Xiaoyong Guo


On x86/x86\_64 platforms (>= i486), 
a CPU core can assert a LOCK signal so that only this core 
can modify the content of a particular memory address.
There are a few instructions that can be prefixed with `lock`.
One such instructions is `cmpxchg`, which is usually used to implement locks
such as mutex.

`cmpxchg` stands for **compare and exchange**. 
It has two operands, the first operand can be a register or memory address,
the second operand is register. What `cmpxchg` actually does is shown in the following code:

```c++
// cmpxchg r/m (v), r (b)
if (eax == v) {

    zf = 1;
    v = b;

} else {

    zf = 0;
    eax = v;
}
```

**compare and exchange** is more commonly called  **compare and swap** or `CAS` operation in some literatures.
It is a very important technique to do synchronization between threads.
The semantics of **compare and exchange** is: I think `V` should be `A`, if it is, 
then set `V` to `B` and return true, otherwise, return false. If written in C, it should
look like this:

```c++
bool compare_and_swap (int* m, int expected, int val) {

    if (*m == expected) {

        *m = val;
        return true;
    }

    return false;
}
```

In C++11, `atomic_compare_exchange_weak` and `atomic_compare_exchange_strong`
does the same thing. Actually, they are wrappers of `lock cmpxchg` on x86/x86_64 platform.
GCC provide [buildin functions for atomic memory access](https://gcc.gnu.org/onlinedocs/gcc-4.1.2/gcc/Atomic-Builtins.html).
Two of them are related to `cmpxchg` instruction:

```c++
bool __sync_bool_compare_and_swap (type *ptr, type oldval type newval, ...)
type __sync_val_compare_and_swap (type *ptr, type oldval type newval, ...)
```

We can build our own lock using these functions. Following is an example.


```c++
/* a customer built spinlock, using __sync_bool_compare_and_swap */
struct SpinLock {

    int flag;
    int lock_flag;
    int unlock_flag;

    SpinLock(): flag(0), lock_flag(1), unlock_flag(0) {
    }

    void lock() {

        while (!__sync_bool_compare_and_swap(&flag, unlock_flag, lock_flag));

#if 0
        /* except for atomicity
           the following while code block has the same effect 
           as __sync_bool_compare_and_swap */
        while (true) {

            if (flag == unlock_flag) {
                flag = lock_flag;
                break;
            }
        }
#endif

    }

    void unlock() {

        flag = unlock_flag;
    }
};
```

We can also implement `SpinLock` using `std::atomic<int>` class, as shown 
in the following code:

```c++
#include <atomic>

struct SpinLock {

    std::atomic<int> flag;

    SpinLock(): flag(0) {
    }

    void lock() {

        int unlock_flag = 0;
        int lock_flag = 1;

        do {

            unlock_flag  = 0;

        } while (!flag.compare_exchange_strong(unlock_flag, lock_flag));
    }

    void unlock() {

        flag = 0;
    }
};
```

Now we can use this `SpinLock` in our code to do synchronization.

```c++
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/syscall.h>
#include <sys/types.h>

int a = 0;
pthread_mutex_t mutex;
SpinLock spinlock;

void* pfun(void* arg) {

    printf("pid = %d\n", syscall(SYS_gettid));

    int n = 0;
    for (n = 0; n < 10000; n++) {
        //pthread_mutex_lock(&mutex);
        spinlock.lock(); // use our spinlock to replace pthread_mutex
        a++;
        spinlock.unlock();
        //pthread_mutex_unlock(&mutex);
    }

    return NULL;
}

int main(void) {

#define NUM_THREAD 10

    printf("pid = %d\n", getpid());
    printf("pid = %d\n", syscall(SYS_gettid));

    pthread_t p[NUM_THREAD];
    pthread_mutex_init(&mutex, NULL);

    int n;
    for (n = 0; n < NUM_THREAD; n++) {

        pthread_create(p+n, NULL, pfun, NULL);
    }

    for (n = 0; n < NUM_THREAD; n++) {

        pthread_join(p[n], NULL);
    }

    pthread_mutex_destroy(&mutex);
    printf("a = %d\n", a);

    return 0;
}
```

## References
1. [C11 Lock-free Stack](http://nullprogram.com/blog/2014/09/02/)
2. [Compare-and-swap](https://en.wikipedia.org/wiki/Compare-and-swap)
