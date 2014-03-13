# demonstration of fitting a function to data
from math import sqrt, pi
import numpy

from scipy.optimize import leastsq
from numpy.polynomial import Polynomial
from numpy.polynomial.chebyshev import Chebyshev

from numpy.random import normal, uniform
from matplotlib import pyplot

colors='bgrcmy'*100

def fit_example(nset=5, order=9):
    # create some example data
    xmin, xmax = 4000.0, 5000.0
    deltax = 25.0
    wl = numpy.arange(xmin, xmax, deltax)
    nwl = len(wl)
    f = gaussian(wl, 0.75, 4750.0, 150.0)
    x = numpy.array([])
    y = numpy.array([])
    id = numpy.array([], numpy.int)
    pyplot.ion()
    pyplot.close('all')
    psim = numpy.zeros(2*nset+order)
    offsets = []
    scales = []
    for i in range(nset):
        offset = uniform(-0.2, 0.2)
        offsets.append(offset)
        scale = uniform(0.8, 1.2)
        scales.append(scale)
        x = numpy.concatenate((x, wl))
        yi = offset + scale * f
        pyplot.plot(wl, yi, '--', color=colors[i])
        # add some noise to the simulated data
        yi += normal(0.0, 0.1, nwl)
        y = numpy.concatenate((y, yi))
        id = numpy.concatenate((id, i*numpy.ones(nwl, numpy.int)))
        pyplot.plot(wl, yi, 'o', color=colors[i], mec='w')
    avoffset = numpy.mean(offsets)
    avscale = numpy.mean(scales)
    print '\nSimulated:'
    print '%8s %8s %8s %8s %8s'%('id', 'offset', 'scale', 'rel.offset', 'rel.scale', )
    for i in range(nset):
        print '%8i %8.3f %8.3f %8.3f %8.3f'%(i, offsets[i], scales[i], offsets[i]-avoffset, scales[i]/avscale)
    # do the fit
    results = fit(x, y, id, nset, order, xmin, xmax)
    # output results
    if results is None:
        print 'Fit failed!'
    else:
        val, err = results
        offsets = val[:nset]
        scales = val[nset:2*nset]
        coeffs = val[2*nset:]
        offsets_err = err[:nset]
        scales_err = err[nset:2*nset]
        coeffs_err = err[2*nset:]
        # errors using this routine are wrong
        # could perhaps be fixed, or could use bootstrap
        # e.g. https://github.com/cgevans/scikits-bootstrap
        avoffset = numpy.mean(offsets)
        avscale = numpy.mean(scales)
        print '\nFitted:'
        print '%8s %8s %8s %8s %8s'%('id', 'offset', 'scale', 'rel.offset', 'rel.scale', )
        for i in range(nset):
            print '%8i %8.3f %8.3f %8.3f %8.3f'%(i, offsets[i], scales[i], offsets[i]-avoffset, scales[i]/avscale)
        coef = Chebyshev(coeffs, domain=(xmin, xmax)).convert(kind=Polynomial, domain=(xmin, xmax)).coef
        str = ''
        for p, c in enumerate(coef):
            if p == 0:
                str += '%.5f'%c
            elif p == 1:
                str += ' + %.5f * x'%c
            else:
                str += ' + %.5f * x**%i'%(c, p)
        print '\nf(x) =', str
        print 'where x = ((wl - %.5f)/%.5f) - 1\n'%(xmin, (xmax-xmin)/2.0)
        x = (2*(wl - xmin)/(xmax-xmin)) - 1
        f = eval(str)
        pyplot.plot(wl, f, '-k', linewidth=3)

def fit(x, y, id, nset, order, xmin, xmax):
    # x and y are data points
    # id identifies the set each data point is from (numbered 0 to nset-1)
    offsets = numpy.zeros(nset, numpy.float)
    scales = numpy.ones(nset, numpy.float)
    coeffs = numpy.zeros(order, numpy.float)
    coeffs[0] = 0.3
    coeffs[1] = 0.3
    coeffs[2] = -0.1
    p0 = numpy.concatenate((offsets, scales, coeffs))
    #plot_func(p0, nset, xmin, xmax, ':')
    args = (y, x, nset, id, xmin, xmax)
    plsq = leastsq(residuals, p0, args=args, full_output=True)
    (popt, pcov, infodict, errmsg, ier) = plsq
    #print errmsg
    if pcov is None:
        print 'Singular matrix encountered - infinite covariance'
        return None
    else:
        s_sq = (residuals(popt, *args)**2).sum()/(len(y)-len(p0))
        pcov = pcov * s_sq
        perr = numpy.sqrt([pcov[i,i] for i in range(len(popt))])
        plot_func(popt, nset, xmin, xmax)
        return popt, perr
    

def function(p, x, nset, id, xmin, xmax):
    offset = p[id]
    scale = p[nset + id]
    coeffs = p[2*nset:]
    f = Chebyshev(coeffs, domain=(xmin, xmax))
    return offset + scale * f(x)

def residuals(p, y, x, nset, id, xmin, xmax):
    res = y - function(p, x, nset, id, xmin, xmax)
    #print 'chisq =', (res**2).sum()
    return res

def gaussian(x, ampl, centre, sigma):
    # with unit maximum
    return ampl * numpy.exp(-(x-centre)**2/(2.0*sigma**2))

def plot_func(p, nset, xmin, xmax, ls='-'):
    nwl = 1001
    wlr = numpy.arange(xmin, xmax+0.5/nwl, float(xmax-xmin)/(nwl-1))
    for i in range(nset):
        idr = i*numpy.ones(nwl, numpy.int)
        yr = function(p, wlr, nset, idr, xmin, xmax)
        pyplot.plot(wlr, yr, linestyle=ls, color=colors[i])
