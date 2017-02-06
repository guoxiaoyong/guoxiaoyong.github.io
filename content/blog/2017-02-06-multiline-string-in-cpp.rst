==============================
Multiline String in C and C++
==============================

:date: 2017-02-06

Sometimes we want to hardcode a multi-line string directly into the C/C++ 
source code. For example, the usage message is often hardcoded into the 
source code. Of course we can use line continuation feature of C/C++ by 
adding a ``\`` sign at the end of a line, but in my opinion, it often makes 
the code looks rather messy. From early time on, C considers two or more 
adjacent string literals as one single string, so we can use this feature to make 
the code more readable. The following is an example.

.. code-block:: cpp

  #include <stdio.h>

  const char* poem =
  "The Purple Cow\n"
  "\n"
  "author: Gelett Burgess\n"
  "\n"
  "I never saw a Purple Cow,\n"
  "I never hope to see one,\n"
  "But I can tell you, anyhow,\n"
  "I'd rather see than be one!";

  int main(void) {
    printf("%s\n", poem);
    return 0;
  }

One problem with this approach is that we need to put each line in a pair of 
quotation marks ``"``, and we need to escape specially characters such as 
quotation mark ``"`` itself. Sometimes, we need to embed a json string 
in the source code of a unittest, then it could turn out to be really annoying,
you need to write many ``\"`` since json's object/dictionary keys are 
always strings. A better way to write multi-line string is to take advantage 
of C/C++ preprocessor's stringification feature and variadic macro feature.
We can rewrite the above code using this new approach.

.. code-block:: cpp

  #include <stdio.h>

  #define MULTILINE_String(...) #__VA_ARGS__

  const char* poem = MULTILINE_String(
  The Purple Cow\n
  \n
  author: Gelett Burgess\n
  \n
  I never saw a Purple Cow,\n
  I never hope to see one,\n
  But I can tell you, anyhow,\n
  I would rather see than be one!
  );

  int main(void) {
    printf("%s\n", poem);
    return 0;
  }

This form is a lot easier to write, we don't need to write quotation marks 
for each line. But we still need to write ``\n`` for each line if newline 
character is significant. In some cases, such as json strings, we can safely 
omit ``\n``.  One problem with this approach is that it cannot handle 
the charater ``'``. I didn't find any solution to include **I'd** in the 
string using this method. So I modified **I'd** to **I would** in the poem.

In C++11, we have an even better way to write multi-line strings.
C++11 introduced raw string literals. You can simply put unescaped 
string between ``R"(`` and ``)"``. You can also add your own delimiter.
Using this newly introduce feature, we can rewrite the above code as:

.. code-block:: cpp

  #include <cstdio>

  const char* poem = R"(
  The Purple Cow

  author: Gelett Burgess

  I never saw a Purple Cow,
  I never hope to see one,
  But I can tell you, anyhow,
  I'd rather see than be one!
  )";

  int main(void) {
    printf("%s\n", poem);
    return 0;
  }


----------
Reference
----------
1. `On Concatenating Adjacent String Literals <http://softwareengineering.stackexchange.com/questions/254984/on-concatenating-adjacent-string-literals>`_
2. `C++ String Literal <http://en.cppreference.com/w/cpp/language/string_literal>`_
