# sdss_to_maggies.py

# Functions to convert SDSS pipeline magnitudes (actually asinh
# luptitudes, as obtained from the SkyServer) into AB, Galactic
# extintion corrected maggies for use with Mike Blanton's kcorrect
# program.

# This code is an adaptation of the files sdss_to_maggies.pro,
# k_sdssfix.pro, k_sdss_err2ivar, k_lups2maggies, k_minerror, k_abfix
# from the kcorrect package, v4_1_4.

# Written by Steven Bamford.
# Started 7 June 2006.

# RCS version control header:--------------------------------------------------
# 	$Id$
#------------------------------------------------------------------------------

import numpy as N

bvalues=N.array([1.4e-10, 0.9e-10, 1.2e-10, 1.8e-10, 7.4e-10])
errband=N.array([0.05, 0.02, 0.02, 0.02, 0.03])
aboff=N.array([-0.036, 0.012, 0.010, 0.028, 0.040])

def sdss_to_maggies_array(magnitudes, mag_errors, extinction):
    """Convert an array of SDSS magnitudes.

    Convert an array of SDSS pipeline magnitudes (actually asinh
    luptitudes) into AB, Galactic extintion corrected maggies.  The
    magnitudes array must have the shape (n, 5), with the five sdss
    magnitudes in the order u,g,r,i,z.  The mag_errors and extinction
    arrays must have shape (n, 5) and contain the corresponding
    magnitude uncertainties and extinctions (in magnitudes),
    respectively"""
    
    # check array shapes
    if magnitudes.shape[1] =! 5:
	print 'Error: array must have shape (n, 5)'
	return
    if magnitudes.shape[0] == 0:
	print 'Error: no data in array'
	return
    if mag_errors.shape != magnitude.shape:
	print 'Error: shapes of extinction and magnitude'
	print '       arrays do not match'
	return
    if extinction.shape != magnitude.shape:
	print 'Error: shapes of extinction and magnitude'
	print '       arrays do not match'
	return
    # extinction correction
    magnitudes = magnitudes - extinction
    # convert errors to inverse variances and fix "bad" values
    mag_ivar = err_to_ivar(mag_errors)
    # enforce minimum magnitude error, i.e. maximum inverse variance
    ivarband = 1/(errband**2)
    N.putmask(mag_ivar, mag_ivar > ivarband, ivarband)
    # where magnitudes have "bad" values, in case they haven't already
    # been flagged in the errors, set ivar=0
    error_index = magnitudes < -99
    N.putmask(mag_ivar, error_index, 0.0)
    # convert to maggies
    maggies, maggies_ivar = lups_to_maggies(magnitudes, mag_ivar)
    # convert to AB maggies
    maggies = maggies * 10.0**(-0.4*aboff)
    maggies_ivar = maggies_ivar * 10.0**(0.8*aboff)
    return maggies, maggies_ivar
    

def err_to_ivar(err):
    """Convert an array of errors to inverse variances."""
    ivar = N.ones(err.shape, N.Float)
    # Errors < 0 imply "bad" measurements: set ivar=0
    error_index = err <= 0.0
    N.putmask(err, error_index, 1.0)  # to make safe for reciprocal
    N.putmask(ivar, error_index, 0.0)
    ivar = ivar * 1.0/err
    return ivar
    

def lups_to_maggies(luptitudes, lup_ivar):
    """Convert SDSS luptitudes (asinh magnitudes) to maggies.

    Conversion from luptitudes to maggies is:
    maggies = 2*b*sinh(-ln(b) - 0.4*ln(10)*lups)
    Conversion of the errors is:
    maggies_err = 2*b*cosh(-ln(b) - 0.4*ln(10)*lups)*0.4*ln(10)*lups_err"""
    
    mask = close_to_zero(lup_ivar)
    # mask bad values
    N.putmask(luptitudes, mask, 1.0)
    N.putmask(lup_ivar, mask, 1.0)
    lup_err = N.sqrt(1.0/lup_ivar)
    print 'Needs testing of bvalues broadcasting'
    maggies = 2.0*bvalues*N.sinh(-N.log(bvalues)-0.4*N.log(10.0)*luptitudes)
    maggies_err = N.cosh(-N.log(bvalues)-0.4*N.log(10.0)*luptitudes)
    maggies_err *= 2.0*bvalues*0.4*N.log(10.0)*lup_err
    maggies_ivar = 1.0/maggies_err**2
    # mask bad values
    N.putmask(maggies, mask, 0.0)
    N.putmask(maggies_ivar, mask, 0.0)
    return maggies, maggies_ivar


def close_to_zero(a):
    """Select array elements which are close to zero.

    Returns Boolean array corresponding to where elements in the input
    array are close to zero, as judged by the precision of the
    single type."""
    
    precision = 10**-8
    return N.logical_and(a<precison, a>-precision)
