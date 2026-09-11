#include <iostream>
using namespace std;

int main()
{
  int n;
  cout << "Enter the value of n: ";
  cin >> n;

  // Example of a loop with O(n) time complexity
  for (int i = 0; i < n; i++)
  {
    cout << i << endl;
  }
  cout << endl;

  return 0;
}