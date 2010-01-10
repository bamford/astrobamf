
# Adapted from IDL code written by Enrico Marchetti, ESO, January 2001
# obtained from http://www.eso.org/gen-fac/pubs/astclim/lasilla/diffrefr.html

import numpy as N
from gaussian import gaussian2d
from checkarray import checkarray
from ppgplot_spb import *

def dar(AM, lam, lam0=5000.0, TC=11.5, RH=44.2, P=772.2):    
    """The routines computes the Differential Atmospheric Dispersion
       in arcsec for a given airmass 'AM' and wavelength 'lam'
       with respect to a reference wavelength 'lam0'.

       The atmospheric parameters can be adjusted to those characterstic
       of the site the computation is made for:
       TC = Temperature [C], RH = Relative Humidity [%], P = Pressure [mbar].
       The default parameters refer to the average La Silla conditions.
    """
    ZD = N.arccos(1.0/AM)

    T = TC+273.16

    PS = -10474.0+116.43*T-0.43284*T**2+0.00053840*T**3

    P2 = RH/100.0*PS
    P1 = P-P2

    D1 = P1/T*(1.0+P1*(57.90*1.0e-8-(9.3250*1.0e-4/T)+(0.25844/T**2)))
    D2 = P2/T*(1.0+P2*(1.0+3.7e-4*P2)*(-2.37321e-3+(2.23366/T)-(710.792/T**2)+(7.75141e4/T**3)))

    S0 = 1.0e4/lam0
    S = 1.0e4/lam

    N0_1 = 1.0e-8*((2371.34+683939.7/(130-S0**2)+4547.3/(38.9-S0**2))*D1+
                   (6487.31+58.058*S0**2-0.71150*S0**4+0.08851*S0**6)*D2)

    N_1 = 1.0e-8*((2371.34+683939.7/(130-S**2)+4547.3/(38.9-S**2))*D1+
                  (6487.31+58.058*S**2-0.71150*S**4+0.08851*S**6)*D2)

    DR = N.tan(ZD)*(N0_1-N_1)*206264.8

    return DR

def dar_corr(airmass, slit, fwhm, lam, diffang=90.0,
             lam0=5000.0, TC=11.5, RH=44.2, P=772.2,
             show=False, n=10):
    """Returns ratio of the volume of a 2D Gaussian of given fwhm
       contained within a slit of given width, with a shift from centre
       of slit corresponding to differential refraction expected given
       specified wavelength and conditions, versus same with no shift.
       All distances in arcsec.
    """
    dr = dar(airmass, lam, lam0, TC, RH, P)
    #print 'Differential refraction is %.2f arcsec'%dr
    # use Gaussian with n elements across slit, and 3 times FWHM along slit
    cx = (n-1)/2.0  # centre of slit
    nfs = n*(1.0*fwhm)/slit  # number of elements across fwhm
    nsigs = nfs/2.3548  # number of elements across sigma
    s = max(1, int(3.0*nfs))  # number of elements across 3 fwhm
    cy = (s-1)/2.0  # centre along slit
    ndr = n*(1.0*dr)/slit # diff. refr. shift in elements
    ndr = checkarray(ndr)
    corr = N.zeros(ndr.shape, N.float)
    # no shift
    g = gaussian2d((n,s), 1.0, cy, cx, nsigs, nsigs)
    noshift = g.sum()
    # with shifts
    if show:
        pgopen('/aqt')
        pgsetup()
    for i, ndri in enumerate(ndr):
        ndrix = ndri*N.sin(diffang*N.pi/180.0)
        g = gaussian2d((n,s), 1.0, cy, cx-ndrix, nsigs, nsigs)
        if show:
            pgeras()
            pgswin(-cy*slit/n, cy*slit/n, -cy*slit/n, cy*slit/n)
            pggray_s(g, g.max(), g.min(),
                     -cy*slit/n, -cx*slit/n, cy*slit/n, cx*slit/n)
            pgbox('BCNTS', 0, 0, 'BCNTS', 0, 0)
        corr[i] = g.sum()
    if show:
        pgclos()
    corr /= noshift
    if len(corr) == 1:
        return corr[0]
    else:
        return corr
    
def plot_dar_corr():
    pass
