from ppgplot_spb import *
from math import *
import numarray as N

def plot_nfw():
    pgopen('/aqt')
    pgpap(0.0, 1.0)
    pgslw(3)
    xlow, xhigh = 0.0, 1.0
    ylow, yhigh = 0.0, 1.5
    npoints = 100
    pgenv(xlow, xhigh, ylow, yhigh)
    x = N.arange(1,npoints+1) * (xhigh - xlow) / npoints + xlow
    ci = 2
    for c in [5, 10, 15]:
	y = vc_v200_nfw(x, c)
	#y = y / y[int(200/c)]
	ci += 1
	pgsci(ci)
	pgline(x*c/10.0, y)
    pgclos()

def vc_v200_nfw(x, c):
    top = N.log(1.0 + c*x) - c*x / (1.0 + c*x)
    bottom = N.log(1.0 + c) - c / (1.0 + c)
    vc2 = top / (x * bottom)
    vc = N.sqrt(vc2)
    return vc

