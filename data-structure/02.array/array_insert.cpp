#include <iostream>
using namespace std;

int main()
{
  int a[10] = {10, 20, 30, 40, 50};
  int length = 5;
  int pos = 2;
  int value = 25;
  for (
      int i = length; i > pos; i--)
    a[i] = a[i - 1];
  a[pos] = value;
  length++;
  return 0;
}