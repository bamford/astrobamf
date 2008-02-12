from rpy import r, set_default_mode, NO_CONVERSION, PROC_CONVERSION

import numpy as N
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d

from ppgplot_spb import *
import gaussian

set_default_mode(PROC_CONVERSION)

def bootdensity(data, min, max, nboot, ci):
    """ Calculate density and confidence intervals on density
    for a 1D array of points.  Bandwidth is selected automatically.
    """
    r("""
      limdensity <- function(data, weights=NULL, bw="nrd0")
      {
        density(data, from=%f, to=%f, weights=weights, bw=bw)
      }
      """%(min, max))
    density = r.limdensity(data)
    xdens = N.array(density['x'])
    ydens = N.array(density['y'])
    bw = density['bw']
    #print 'bandwidth:', bw
    ydensboot = N.zeros((nboot, len(xdens)), N.float)
    ndata = len(data)
    ran = N.random.uniform(0, ndata, (nboot,ndata)).astype(N.int)
    for i in range(nboot):
        den = r.limdensity(data[ran[i]])
        y = N.array(den['y'])
        ydensboot[i] = y
    ydensbootsort = N.sort(ydensboot, axis=0)
    ydensbootsort = interp1d(N.arange(0, 1.000001, 1.0/(nboot-1)),
                             ydensbootsort, axis=0)
    ilow = (0.5-ci/2.0)
    ihigh = (0.5+ci/2.0)
    ydenslow, ydenshigh = ydensbootsort((ilow, ihigh))
    ydenslow = gaussian_filter1d(ydenslow, bw*512/10.0)
    ydenshigh, ydenshigh = ydensbootsort((ihigh, ihigh))
    ydenshigh = gaussian_filter1d(ydenshigh, bw*512/10.0)
    return xdens, ydens, ydenslow, ydenshigh, bw

def test():
    a = N.random.normal(0.0, 1.0, 500)
    hist = r.hist(a)
    breaks = N.array(hist['breaks'])
    dhist = N.zeros(breaks.shape, N.float)
    dhist[:-1] = hist['density']
    xdens, ydens, ydenslow, ydenshigh = bootdensity(a, -5.0, 5.0, 100, 0.95)
    xg = (N.arange(1000) / 500.0 - 1.0) * 5.0
    yg = gaussian.gaussian(xg, 1.0, 0.0, 1.0)
    pgaqt()
    pgsetup()
    pgenv(-5.0, 5.0, 0.0, 0.5)
    pgbin(breaks, dhist, False)
    pgxsci('yellow')
    pgbin(breaks, dhist-2*(N.sqrt(dhist*1000)/1000.0), False)
    pgbin(breaks, dhist+2*(N.sqrt(dhist*1000)/1000.0), False)
    pgxsci('black')
    pgline(xdens, ydens)
    #pgxsci('lightgray')
    #for i in range(100):
    #    pgline(xdens, ydensboot[i])
    pgxsci('green')
    pgline(xdens, ydenslow)
    pgxsci('red')
    pgline(xdens, ydenshigh)
    pgxsci('blue')
    pgline(xg, yg)
    pgclos()
