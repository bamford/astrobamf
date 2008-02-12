#include <cstdlib>
#include <iostream>
#include "NRgdev.h"

using namespace std;

int main() 
{ 
  long* idum = new long(123);
  for (int i = 0; i < 1000000; i++)
    {
      cout << NRgdev(idum) << "  " << *idum << endl;
    }
}
