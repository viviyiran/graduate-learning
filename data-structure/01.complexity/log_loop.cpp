#include <iostream>
using namespace std;

int main()
{
  int n;
  cout << "enter n:";
  cin >> n;
  // 时间复杂度是O(log n)
  for (int i = 1; i <= n; i = i * 2)
  {
    cout << i << endl;
  }
  return 0;
}