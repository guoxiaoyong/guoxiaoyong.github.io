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
I would rather see than be one!);

int main(void) {
  printf("%s\n", poem);
  return 0;
}
