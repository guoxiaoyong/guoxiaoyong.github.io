---
layout: post
title: "Build Your Own Conditional Variable"
date: 2016-07-28 08:37:45 +0800
categories: C++
---

**Xiaoyong Guo**

In my blog post [How do Locks work]({% post_url 2016-07-26-how-do-locks-work %}),
I gave examples of building a **spin lock** based on basic `CAS` atomic operation
provided by CPU. Another very importance synchronization construct in concurrent programming is
[conditional variable](https://en.wikipedia.org/wiki/Monitor_%28synchronization%29).
In the following example, I give an example of 
a Homebrew conditional variable class built on top of our `SpinLock` class.
It is actually quite simple.

{% highlight c++ %}

/* a customer built spinlock, using __sync_bool_compare_and_swap */
class SpinLock {

private:
    int flag;

public:
    SpinLock(): flag(0) {}

    void lock() {

        while (!__sync_bool_compare_and_swap(&flag, 0, 1));
    }

    void unlock() {

        flag = 0;
    }
};


/* condition variable class */
class CondVariable {

private:
    volatile int flag; // revised on 2016-07-29
    // std::atomic<int> flag; // C++11 recommend using this form

public:
    CondVariable():flag(0) {}

    int wait(SpinLock& spinlock) {

        int id = flag;
        flag++;
        spinlock.unlock();

        while (flag > id); 

        spinlock.lock();
        return 0;
    }

    void signal() {
        flag--;
        flag = (flag>0)*flag;
    }

    void broadcast() {
        flag = 0;
    }
};

{% endhighlight %}

One problem for the above conditional variable class 
is: when `signal` method is called to unblock a thread 
waiting on the conditional variable, the last thread that
called `wait` will be unblocked. 
This may cause problems. Following is a example of using
this conditional variable class. 


{% highlight c++ %}
#include <thread>
#include <mutex>
#include <queue>
#include <iostream>
#include <unistd.h>

using namespace std;

queue<int>    iqueue;
SpinLock      spinlock;
CondVariable  condv;
bool quit = false;

void consumer() {

    while (true) {
        spinlock.lock();

        cout << "consumer queue size = " << iqueue.size() << endl;
        if (iqueue.empty()) {

            condv.wait(spinlock);
        }

        while (!iqueue.empty()) {

            cout << "consume item " << iqueue.front() << endl;
            iqueue.pop();
        }

        spinlock.unlock();
        usleep(std::rand()%256);
        if (quit) break;
    }
}

void producer() {

    while (true) {
        spinlock.lock();

        int d = std::rand()%256;
        iqueue.push(d);
        cout << "produce item: " << d  << endl;
        condv.signal();
        cout << "producer queue size = " << iqueue.size() << endl;

        spinlock.unlock();
        usleep(std::rand()%256);
        if (quit) break;
    }
}

void control() {

    quit = !!getchar();
    spinlock.signal();
}

int main(void) {

    thread t1(consumer);
    thread t2(producer);
    thread t3(control);
    t1.join();
    t2.join();
    t3.join();

    return 0;
}

{% endhighlight %}



