# demonstration of fitting a function to data
from math import sqrt, pi
import numpy as N

from scipy.optimize import leastsq

from numpy.random import normal


def example_fit(nset=5, order=5):
    # create some example data
    wl = numpy.arange(4000, 5000, 1.0)
    f = gaussian(wl, 0.5, 4750.0, 150.0)
    nwl = len(wl)
    x = []
    y = []
    id = []
    for i in range(len(n)):
        offset = numpy.uniform(-0.2, 0.2)
        scale = numpy.uniform(0.8, 1.2)
        print i, offset, scale
        x = numpy.concatenate(x, wl)
        yi = offset + scale * f
        # add some noise to the simulated data
        yi += normal(0.0, 0.2, nwl)
        y = numpy.concatenate(y, yi)
        id = numpy.concatenate(id, i*numpy.ones(nwl))
    results = fit(x, y, id, nset, order)
    if results is None:
        print 'Fit failed!'
    else:
        val, err = results
        offset = val[:nset]
        scale = val[nset:2*nset]
        coeffs = val[2*nset:]
        offset_err = err[:nset]
        scale_err = err[nset:2*nset]
        coeffs_err = err[2*nset:]
        print 'offset:', offset
        print 'offset_err:', offset_err
        print 'scale:', scale
        print 'scale_err:', scale_err
        print 'coeffs:', coeffs
        print 'coeffs_err:', coeffs_err


def fit(x, y, id, nset, order):
    # x and y are data points
    # id identifies the set each data point is from (numbered 0 to nset-1)
    offsets = numpy.zeros(nset, numpy.float)
    scales = numpy.ones(nset, numpy.float)
    coeffs = numpy.zeros(order, numpy.float)
    p0 = numpy.concatenate((offets, scales, coeffs))
    args = (y, x, nset, id, numpy.amin(x), numpy.amax(x))
    plsq = leastsq(residuals, p0, args=args, full_output=True)
    print plsq[3]
    if plsq[1] is None:
        print 'Singular matrix encountered - infinite covariance'
        return None
    else:
        gfit = N.array([float(x) for x in plsq[0]])
        gfit_err = N.array([sqrt(float(plsq[1][i,i])) for i in range(npar)])
        return gfit, gfit_err
    

def function(p, x, nset, id, xmin, xmax):
    offset = p[id]
    scale = p[nset + id]
    coeffs = p[2*nset:]
    f = offset + scale * Chebyshev(coeffs, xmin, xmax)
    return f(x)

def residuals(p, y, x, nset, id, xmin, xmax):
    return y - function(p, x, nset, id, xmin, xmax)

def gaussian(x, ampl, centre, sigma):
    # with unit maximum
    return ampl * N.exp(-(x-centre)**2/(2.0*sigma**2))
