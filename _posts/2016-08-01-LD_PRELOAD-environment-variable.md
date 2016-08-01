---
layout: post
title: "LD_PRELOAD Environment Variable"
date: 2016-08-01 11:57:11 +0800
categories: C++
---

**Xiaoyong Guo**

`LD_PRELOAD` is a environment variable that affects the behavior of dynamic linker/loader. 
According to the man page of `ld.so(8)`:

> **LD_PRELOAD**
> A list of additional, user-specified, ELF shared objects to be loaded before all others.  The items of the list can be separated by spaces or colons.  This can be used to selectively override functions in other shared objects.  The objects are searched for using the rules given under DESCRIPTION.  In secure-execution mode, preload pathnames containing slashes are ignored, and shared objects in the standard search directories are loaded only if the set-user-ID mode bit is enabled on the shared object file.

`LD_PRELOAD` can be used to do various hacks. For example:

{% highlight c %}
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {

    char passwd[] = "password";

    if (argc < 2) {

        printf("usage: %s password\n", argv[0]);
        return 0;
    }

    if (!strcmp(passwd, argv[1])) {

        printf("Correct Password!\n");

    } else {

        printf("Invalid Password!\n");
    }

    return 0;
}
{% endhighlight %}


Compile the above code into a binary executable called **pass**,
if you type the following command, you will get the message "Invalid Password!"

```
./pass hello
```

Let's write a simple `strcmp` function:

{% ighlight c %}
#include <stdio.h>

int strcmp(const char *s1, const char *s2) {

    printf("hack function invoked. s1=<%s> s2=<%s>\n", s1, s2);
    return 0;
}
{% endhighlight %}

Compile the above code into a `so` library `strcmp.so`, then set the environment
`LD_PRELOAD`, the `./pass hello` again, you will get the message "Correct Password!".



