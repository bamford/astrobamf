import numpy as N
from scipy.linalg import cholesky, inv

# Adapted from the SAS code available at
# http://www.ats.ucla.edu/stat/sas/macros/corr2data_demo.htm

def covmat2data(covmat, n, means=None, check=False):
    p = cholesky(covmat)
    dim = covmat.shape[1]
    myvar = N.random.normal(0.0, 1.0, n*dim).reshape((n, dim))
    for i in range(dim):
        myvar[:,i] = myvar[:,i] - myvar[:,i].sum()/n
    XX = (N.dot(myvar.transpose(), myvar))/(n-1)
    U = cholesky(inv(XX))
    Y = N.dot(myvar, U.transpose())
    T = N.dot(Y, p).transpose()
    if means is not None:
        T += means.reshape(means.shape + (1,))
    if check:
        covmatmc = N.cov(T)
        print 'MC covariance matrix OK?', N.all((covmatmc-covmat) < 1e-9)
    return T
