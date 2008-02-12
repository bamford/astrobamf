import fit

def BBfit(x, y, x_err=None, y_err=None, ai=None, bi=None, scatteri=None, clip=None):
    return fit.fit(x, y, x_err, y_err, ai, bi, scatteri, clip, fit_type=2)
