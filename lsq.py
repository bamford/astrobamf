# lsq.py

# Does a least squares fit
# by regressing in the y variable.

# Weights, intrinsic scatter and sigma clipping optional

import numarray as N
import nr_numarray as nr
from math import sqrt

conv_limit = 0.01

def lsq(x, y, sig=None, int_scat=None, clip=None, a=None, b=None, siga_in=0.0, sigb_in=0.0):
    if clip is None or clip == 0:
        if sig is None:
            sig = N.ones(x.shape)
            mwt = 0
        else:
            sig = N.array(sig)
            mwt = 1
        if a is None and b is None:
            if int_scat is None:
                results = nr.fit(x, y, sig)
            else:
                results = nr.fit_i(x, y, sig, int_scat)
            a, b, siga, sigb, chi2 = results
            scatter = calc_scatter(x, y, sig, int_scat, a, b)
        elif a is not None and b is None:
            if int_scat is None:
                results = nr.fit_slope(x, y, sig, mwt, a, siga_in)
            else:
                results = nr.fit_slope_i(x, y, sig, int_scat, a, siga_in)
            b, sigb, chi2 = results
            siga = 0.0
            scatter = calc_scatter(x, y, sig, int_scat, a, b)
        elif a is None and b is not None:
            if int_scat is None:
                results = nr.fit_intercept(x, y, sig, mwt, b, sigb_in)
            else:
                results = nr.fit_intercept_i(x, y, sig, int_scat, b, sigb_in)
            a, siga, chi2 = results
            sigb = 0.0
            scatter = calc_scatter(x, y, sig, int_scat, a, b)
        n = len(x)
        return (a, b, siga, sigb, chi2, scatter, n)
    else:
        return lsq_clipped(x, y, sig, int_scat, clip, a, b, siga_in, sigb_in)


def lsq_clipped(x, y, sig, int_scat=None, clip=3.0, astart=None, bstart=None,
                siga_in=0.0, sigb_in=0.0):
    olda = oldb = None
    if sig is None:
        sig = N.ones(x.shape)
        mwt = 0
    else:
        sig = N.array(sig)
        mwt = 1
    a = astart
    b = bstart
    while 1:
        if astart is None and bstart is None:
            if int_scat is None:
                results = nr.fit(x, y, sig)
            else:
                results = nr.fit_i(x, y, sig, int_scat)
            a, b, siga, sigb, chi2 = results
            scatter = calc_scatter(x, y, sig, int_scat, a, b)
        elif astart is not None and bstart is None:
            if int_scat is None:
                results = nr.fit_slope(x, y, sig, mwt, astart, siga_in)
            else:
                results = nr.fit_slope_i(x, y, sig, int_scat, astart, siga_in)
            b, sigb, chi2 = results
            siga = 0.0
            scatter = calc_scatter(x, y, sig, int_scat, astart, b)
        elif astart is None and bstart is not None:
            if int_scat is None:
                results = nr.fit_intercept(x, y, sig, mwt, bstart, sigb_in)
            else:
                results = nr.fit_intercept_i(x, y, sig, int_scat, bstart, sigb_in)
            a, siga, chi2 = results
            sigb = 0.0
            scatter = calc_scatter(x, y, sig, int_scat, a, bstart)
        if not (olda is None or oldb is None):
            if abs(a) < conv_limit:
                atest = conv_limit
            else:
                atest = abs(a)
            if abs(b) < conv_limit:
                btest = conv_limit
            else:
                btest = abs(b)
            if (abs(olda - a) < conv_limit*atest and
                abs(oldb - b) < conv_limit*btest):
                break
        keep = abs(y - a - b*x) < clip*scatter
        xnew = N.compress(keep, x)
        ynew = N.compress(keep, y)
        signew = N.compress(keep, sig)
        x = xnew
        y = ynew
        sig = signew
        olda, oldb = (a, b)
        n = len(x)
    return (a, b, siga, sigb, chi2, scatter, n)


def calc_scatter(x, y, sig, int_scat, a, b):
    if int_scat is None: int_scat = 0.0
    w = 1.0 / (sig**2 + int_scat**2)
    wSum = N.sum(w)
    varw = N.sum((y - a - b*x)**2 * w) / wSum
    #var = N.sum((y - a - b*x)**2) / len(x)
    stdev = sqrt(varw)
    return stdev
