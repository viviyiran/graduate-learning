#include <iostream>
using namespace std;

int main()
{
  int a[5] = {10, 20, 30, 40, 50};
  int length = 5;
  int index = 2;
  for (int i = index; i < length - 1; i++)
  {
    a[i] = a[i + 1];
  }
  length--;
  for (int i = 0; i < length; i++)
  {
    cout << a[i] << " ";
  }
}