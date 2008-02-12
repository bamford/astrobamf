// NRgdev.h
// Provides a function, NRgdev, which returns
// a random number with a Gaussian probability
// distribution of zero mean and unit standard
// deviation.
// Copied from the advocated routine, gasdev,
// from Numerical Recipes in C, and uses the
// function NRran to produce a uniformly
// random number. This is itself a 
// function recommended by NR.

// This version written 04-12-2002
// by Steven Bamford.

#include <math.h> 
#include "NRran.h"

float NRgdev(long *idum) 
{ 
  static int iset=0;
  static float gset;
  float fac,rsq,v1,v2;
  if (*idum < 0) iset=0;
  if (iset == 0) 
    {
      do 
	{ 
	  v1=2.0*NRran(idum)-1.0;
	  v2=2.0*NRran(idum)-1.0;
	  rsq=v1*v1+v2*v2;
	} while (rsq >= 1.0 || rsq == 0.0);
      fac=sqrt(-2.0*log(rsq)/rsq);
      gset=v1*fac;
      iset=1;
      return v2*fac;
    } 
  else 
    {
      iset=0;
      return gset;
    }
}
