#include <iostream>
#include <climits>
using namespace std;

int main()
{
  int n;
  int max = INT_MIN;
  cin >> n;
  for (int i = 0; i < n; i++)
  {
    int x;
    cin >> x;
    if (x > max)
      max = x;
  }
  cout << max << endl;
  return 0;
}