title: Makefile Arithmetic
date: 2016-08-05 14:57:45 +0800
author: Xiaoyong Guo

**make** is building tool and a programming language. 
It has been proved that **make** as a programming language is [turing complete](https://en.wikipedia.org/wiki/Turing_completeness).
That means, you can write a makefile to do whatever C/java/Python can do, providing that memory is not a concern. 

The following Makefile computes squares, fibonacci numbers and factorials. 

```Makefile
dec = $(patsubst .%,%,$1)

not = $(if $1,,.)

lteq = $(if $1,$(if $(findstring $1,$2),.,),.)
gteq = $(if $2,$(if $(findstring $2,$1),.,),.)
eq = $(and $(call lteq,$1,$2),$(call gteq,$1,$2))
lt = $(and $(call lteq,$1,$2),$(call not,$(call gteq,$1,$2)))

add = $1$2
sub = $(if $(call not,$2),$1,$(call sub,$(call dec,$1),$(call dec,$2)))
mul = $(if $(call not,$2),$2,$(call add,$1,$(call mul,$1,$(call dec,$2))))
fibo = $(if $(call lt,$1,..),$1,$(call add,$(call fibo,$(call dec,$1)),$(call fibo,$(call sub,$1,..))))
fact = $(if $(call lt,$1,..),.,$(call mul,$1,$(call fact,$(call dec,$1))))

numeral = $(words $(subst .,. ,$1))

go = $(or $(info $(call numeral,$(call mul,$1,$1)) $(call numeral,$(call fibo,$1)) $(call numeral,$(call fact,$1)) ),$(call go,.$1))

_ := $(call go,)
```

Another script to compute fabanacci numbers.

```Makefile
16:=x x x x x x x x x x x x x x x x
input_int:=$(foreach a,$(16),$(foreach b,$(16),$(foreach c,$(16),$(16))))
decode=$(words $1)
encode=$(wordlist 1,$1,$(input_int))
decr=$(wordlist 2,$(words $1),$1)
decr2=$(wordlist 3,$(words $1),$1)
eq=$(filter $(words $1),$(words $2))
g0:=
g1:=x
 
fib=$(if $(filter-out undefined,$(origin f$1)),
$(f$1),
$(if $(call eq,$1,$(g0)),
$(eval f$1:=$(g0))$(g0),
$(if $(call eq,$1,$(g1)),
$(eval f$1:=$(g1))$(g1),
$(eval f$1:=$(call fib,$(call decr2,$1)) $(call fib,$(call decr,$1)))$(f$1))))
 
print=$(if $1,
$(call print,$(call decr,$1))$(info $(call decode,$1): $(call decode,$(f$1))),
$(info 0: 0))
 
%:
 
@:$(if x$(call fib,$(call encode,$@)),$(call print,$(call encode,$@)),)
```

## References
1. [Are Makefiles Turing Complete](http://stackoverflow.com/questions/3480950/are-makefiles-turing-complete)
2. [Friday Fun: Generating Fibonacci Numbers with GNU Make](http://electric-cloud.com/blog/2009/08/friday-fun-generating-fibonacci-numbers-with-gnu-make/)
3. [Makefile as a functional language program](http://okmij.org/ftp/Computation/#Makefile-functional)
4. [Learning GNU Make Functions with Arithmetic](https://www.cmcrossroads.com/article/learning-gnu-make-functions-arithmetic)
