import numpy as N

def log10(x, xerr, mask=False):
    z = N.log10(x)
    zerr = N.absolute(xerr * N.log10(N.e)/x)
    if not mask:
        return N.array([z, zerr])
    else:
        ok = x > 0.0
        return N.array([z, zerr]), ok

def pow10(x, xerr, mask=False):
    z = 10**x
    zerr = N.absolute(N.log(10) * xerr * z)
    if not mask:
        return N.array([z, zerr])
    else:
        ok = N.ones(z.shape, N.bool)
        return N.array([z, zerr]), ok        


def multiply(x, xerr, y, yerr, mask=False):
    z = x*y
    zerr = (xerr/x)**2 + (yerr/y)**2
    zerr = N.absolute(N.sqrt(zerr) * z)
    if not mask:
        return N.array([z, zerr])
    else:
        ok = N.ones(z.shape, N.bool)
        return N.array([z, zerr]), ok        

def divide(x, xerr, y, yerr, mask=False):
    z = x/y
    zerr = (xerr/x)**2 + (yerr/y)**2
    zerr = N.absolute(N.sqrt(zerr) * z)
    if not mask:
        return N.array([z, zerr])
    else:
        ok = x != 0.0
        return N.array([z, zerr]), ok

def add(x, xerr, y, yerr, mask=False):
    z = x+y
    zerr = N.absolute((xerr)**2 + (yerr)**2)
    zerr = N.sqrt(zerr)
    if not mask:
        return N.array([z, zerr])
    else:
        ok = N.ones(z.shape, N.bool)
        return N.array([z, zerr]), ok        

def subtract(x, xerr, y, yerr, mask=False):
    z = x-y
    zerr = N.absolute((xerr)**2 + (yerr)**2)
    zerr = N.sqrt(zerr)
    if not mask:
        return N.array([z, zerr])
    else:
        ok = N.ones(z.shape, N.bool)
        return N.array([z, zerr]), ok        

def test():
    n = 100000
    a = 10.0
    aerr = 2.0
    b = 3.0
    berr = 0.3
    x = N.random.normal(a, aerr, n)
    y = N.random.normal(b, berr, n)
    # log10
    t = N.log10(x)
    z, zerr = log10(a, aerr)
    delta = N.absolute(t.mean() - z)/t.mean()
    deltaerr = N.absolute(t.std() - zerr)/t.std()
    print 'log10', delta, deltaerr
    # pow10
    t = 10**y
    z, zerr = pow10(b, berr)
    delta = N.absolute(t.mean() - z)/t.mean()
    deltaerr = N.absolute(t.std() - zerr)/t.std()
    print 'pow10', delta, deltaerr
    # multiply
    t = N.multiply(x, y)
    z, zerr = multiply(a, aerr, b, berr)
    delta = N.absolute(t.mean() - z)/t.mean()
    deltaerr = N.absolute(t.std() - zerr)/t.std()
    print 'multiply', delta, deltaerr
    # divide
    t = N.divide(x, y)
    z, zerr = divide(a, aerr, b, berr)
    delta = N.absolute(t.mean() - z)/t.mean()
    deltaerr = N.absolute(t.std() - zerr)/t.std()
    print 'divide', delta, deltaerr
    # add
    t = N.add(x, y)
    z, zerr = add(a, aerr, b, berr)
    delta = N.absolute(t.mean() - z)/t.mean()
    deltaerr = N.absolute(t.std() - zerr)/t.std()
    print 'add', delta, deltaerr
    # subtract
    t = N.subtract(x, y)
    z, zerr = subtract(a, aerr, b, berr)
    delta = N.absolute(t.mean() - z)/t.mean()
    deltaerr = N.absolute(t.std() - zerr)/t.std()
    print 'subtract', delta, deltaerr
