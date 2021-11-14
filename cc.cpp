#include <stdio.h>
#include <stdlib.h>

int main()
{
  int x;
  for (x = 0; x< 128; x++)
    if (x < 32)
      printf("^%-3c \\x%2.2x \\%3.3o %3d\n", x+64, x, x, x);
    else
      printf("\x20%-3c \\x%2.2x \\%3.3o %3d\n", x, x, x, x);
  fflush(stdout);
  system("cat ascii.c");
} 