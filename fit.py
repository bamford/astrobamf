import numpy as N
import bootbces
import bootsixlin
from math import sqrt
import rostat

def fit_simple(x, y, x_err=None, y_err=None, fit_type=2):
    """ Performs a bivariate, weighted, straight line fit
    with no covariance between the errors. """
    x = N.asarray(x)
    y = N.asarray(y)
    x_err = y_err = None  # don't use weighted fit!
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
    a = float(a[fit_type])
    siga = float(siga[fit_type])
    b = float(b[fit_type])
    sigb = float(sigb[fit_type])
    # determine the scatter
    #scatter = sqrt(N.sum((y-(a+b*x))**2)/len(x))
    # determine the scatter robustly
    scatter = rostat.mad(y-(a+b*x), rostat.median(y-(a+b*x))) / 0.6745
    return a, b, siga, sigb, scatter

def fit(x, y, x_err=None, y_err=None, ai=None, bi=None, scatteri=None, clip=None, fit_type=2):
    conv_limit = 0.0001
    olda = oldb = None
    n = len(x)
    count = 0
    a = ai
    b = bi
    scatter = scatteri
    while 1:
	count += 1
	if None not in [a, b, scatter]:
	    keep = abs(y - a - b*x) < clip*scatter
	    x = N.compress(keep, x)
	    y = N.compress(keep, y)
	    if x_err is not None: x_err = N.compress(keep, x_err)
	    if y_err is not None: y_err = N.compress(keep, y_err)
	a, b, siga, sigb, scatter = fit_simple(x, y, x_err, y_err, fit_type)
	if clip is None: break
	if None not in [olda, oldb]:
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
	olda, oldb = (a, b)
    nclip = len(x)
    print 'fit: %i iterations, %i points rejected, %i remaining'%(count, n-nclip, nclip)
    return a, b, siga, sigb, scatter

def BBfit(x, y, x_err=None, y_err=None, ai=None, bi=None, scatteri=None, clip=None):
    # bisector
    return fit(x, y, x_err, y_err, ai, bi, scatteri, clip, fit_type=2)

def OLSfit(x, y, x_err=None, y_err=None, ai=None, bi=None, scatteri=None, clip=None):
    # OLS(Y|X)
    return fit(x, y, x_err, y_err, ai, bi, scatteri, clip, fit_type=0)

def OLSXYfit(x, y, x_err=None, y_err=None, ai=None, bi=None, scatteri=None, clip=None):
    # OLS(X|Y)
    return fit(x, y, x_err, y_err, ai, bi, scatteri, clip, fit_type=1)
