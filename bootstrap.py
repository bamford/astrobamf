import numpy as N
from scipy.stats import scoreatpercentile
from scipy.interpolate import interp1d

def mean(x):
    return x.sum()/len(x)

def bootstrap(x, nboot=100, f=mean):
    # bootstrap the error on f(x)
    n = len(x)
    m = N.zeros(nboot, N.float)
    for i in range(nboot):
        r = N.random.uniform(0, n, n).astype(N.int)
        b = x[r]
        m[i] = f(b)
    ftrue = f(x)
    ferr = m.std()
    m.sort()
    minterp = interp1d(N.arange(0, 100.000001, 100.0/(nboot-1)), m)
    f1siglow = minterp(16)
    f1sighigh = minterp(84)
    f2siglow = minterp(2.5)
    f2sighigh = minterp(97.5)
    f3siglow = minterp(0.15)
    f3sighigh = minterp(99.85)
    print 'Bootstrap (%i samples)'%nboot
    print 'f(x) = %.3f'%ftrue
    print 'boostrap standard deviation of f(x) = %.3f'%ferr
    print '1 sigma confidence interval on f(x): %.3f - %.3f (half width = %.3f)'%(f1siglow, f1sighigh, (f1sighigh - f1siglow)/2.0)
    return ferr

