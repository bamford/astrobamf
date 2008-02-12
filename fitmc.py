# OLS fit with Monte Carlo parameter errors and covariance,
# assuming accurately known Gaussian errors on the data points
# and known residuals correlation.

import numpy as N
import sixlin

def fitmc(x, xerr, y, yerr, cor=None, nmc=1000):
    n = len(x)
    afit = N.zeros(nmc, N.float)
    bfit = N.zeros(nmc, N.float)
    if cor is None:
        cor = x*0.0
    for i in range(nmc):
        r1 = N.random.normal(0.0, 1.0, n)
        r2 = N.random.normal(0.0, 1.0, n)
        xr = x + r1*xerr
        yr = y + (cor*r1 + (1-cor)*r2) * yerr
        fit = sixlin.sixlin(xr, yr)
        a, siga, b, sigb = fit
        afit[i] = a[0]
        bfit[i] = b[0]
    fit = sixlin.sixlin(x, y)
    a, siga, b, sigb = fit
    a = a[0]
    b = b[0]
    siga = afit.std()
    sigb = bfit.std()
    corab = ((afit - afit.mean())*(bfit - bfit.mean())).sum()
    corab /= (nmc-1)*siga*sigb
    return a, siga, b, sigb, corab, afit, bfit
