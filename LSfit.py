
import numpy as N
import bootbces
import bootsixlin
from math import sqrt

def LSfit(x, y, x_err=None, y_err=None):
    """ Performs a bivariate, weighted, bisector fit
    with no covariance between the errors. """
    x = N.asarray(x)
    y = N.asarray(y)
    nsample = 100
    seed = 34895672
    if x_err is None or y_err is None:
	print 'Performing unweighted bisector fit'
	a,siga,b,sigb = bootsixlin.bootsixlin(x, y, nsample, seed)
    else:
	print 'Performing weighted bisector fit'
	x_err = N.asarray(x_err)
	y_err = N.asarray(y_err)
	cerr = x*0.0
	a,b,siga,sigb = bootbces.bootbces(x, x_err, y, y_err, cerr, nsample, seed)
    # use the OLS(X|Y) fit:
    fit_type = 0
    a = float(a[fit_type])
    siga = float(siga[fit_type])
    b = float(b[fit_type])
    sigb = float(sigb[fit_type])
    # determine the scatter
    scatter = sqrt(N.sum((y-(a+b*x))**2)/len(x))
    return a, b, siga, sigb, scatter
