#include <iostream>
using namespace std;
void swap1(int &x, int &y)
{
  int tmp = x;
  x = y;
  y = tmp;
  return;
}
int main()
{
  int a;
  int b;

  cout << "请输入一个整数: ";
  cin >> a;
  cout << "请输入一个整数: ";
  cin >> b;
  cout << "before: " << a << " " << b << endl;
  swap1(a, b);
  cout << "after: " << a << " " << b << endl;
  return 0;
}