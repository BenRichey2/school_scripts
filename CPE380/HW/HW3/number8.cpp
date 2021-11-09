#include <iostream>
using namespace std;
int a=380, b=480, c=42;
void f(int x, int &y, int *z) { ++x; ++y; ++*z; }
int main() {
      cout <<"a="<<a <<" b="<<b <<" c="<<c <<endl;
        f(a,b,&c);
          cout <<"a="<<a <<" b="<<b <<" c="<<c <<endl;
}
