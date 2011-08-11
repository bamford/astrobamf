# metallicity.py

# Functions for calculating line indicies and
# hence [O/H] metallicity following
# Kobulnicky et al. 2003 ApJ 599 1006 [K03]
# Kobulnicky & Pierce 2003 ApJ 599 1031 [KP03]
# Kobulnicky & Kewley 2004

from math import *
import time
from scipy.optimize import fmin, leastsq
import numpy as N
import numpy.random as RA
from ppgplot_spb import *

def R23(EW3727, errEW3727, EW4959, errEW4959,
        EW5007, errEW5007, EW4861, errEW4861):
    # Compute the oxygen abundance indicator R23 as
    # defined for line fluxes by Pagel et al. (1979),
    # but shown to be valid for EWs by [KP03].
    top = EW3727 + EW4959 + EW5007
    err_top = N.sqrt(errEW3727**2 + errEW4959**2 + errEW5007**2)
    bottom = EW4861
    err_bottom = errEW4861
    ratio = top / bottom
    err_ratio = N.sqrt((err_top/top)**2 + (err_bottom/bottom)**2) * ratio
    return ratio, err_ratio


def O32(EW4959, errEW4959, EW5007, errEW5007,
        EW3727, errEW3727):
    # Compute the ionisation parameter O32 as
    # given in [KP03] for fluxes and shown to be
    # valid for EWs upto a factor, alpha, which
    # is approximately unity.
    top = EW4959 + EW5007
    err_top = N.sqrt(errEW4959**2 + errEW5007**2)
    bottom = EW3727
    err_bottom = errEW3727
    ratio = top / bottom
    err_ratio = N.sqrt((err_top/top)**2 + (err_bottom/bottom)**2) * ratio
    return ratio, err_ratio


# NEED TO IMPLEMENT METHOD FOR DEALING WITH POINTS OFF THE
# CALIBRATION AS DISCUSSED WITH JOHN.

def oxygen_abundance(R23, O32, KK04=False, recover=False, branch='high'):
    # Compute the oxgen abundance 12 + log(O/H)
    # using the analytical expressions of McGaugh (1991, 1998)
    # as given in [K03],
    # or optionally the expressions of Kobulnicky & Kewley (2004)
    x0 = x = log10(R23[0])
    xerr = R23[1] / R23[0] / log(10)
    y0 = y = log10(O32[0])
    yerr = O32[1] / O32[0] / log(10)
    # check that R23 is within the calibration limits, given O32
    if KK04:
	xlimit = xlimit_KK04(y)
    else:
	xlimit = xlimit_M91(y)
    warning = 0
    if recover:
	sigma = 0.0
	deltasigma = 0.1
	if x > xlimit:
	    print 'R23 and O32 outside oxyab calibration limits'
	    print 'Attempting to adjust R23 and O32 within their 5-sigma'
	    print 'uncertainities to find valid values'
	    warning = 1
	while x > xlimit:
	    sigma += deltasigma
	    # problem: calibration not defined for R23 this high at this O32
	    # check to see whether makes sense within R23 errors
	    if x - deltasigma*xerr < xlimit:
		# adjusting R23 within its errors worked
		x = x - deltasigma*xerr
		break
	    else:
		# if adjusting R23 hasn't helped, check whether adjusting
		# O32 within its errors moves the limit enough
		y = y + deltasigma*yerr
		if KK04:
		    xlimit = xlimit_KK04(y)
		else:
		    xlimit = xlimit_M91(y)
	    if x < xlimit:
		# adjusting O32 within its errors worked
		break
	    else:
	       x = x - deltasigma*xerr 
	    if sigma > 5.0:
		print 'Failed to find a solution by adjusting R23 and O32'
		print 'within their 5-sigma errors'
		return None
	if sigma > deltasigma/2.0:
	    xshift = (x-x0)/xerr
	    yshift = (y-y0)/yerr
	    xerr = xerr*max(1.0, abs(xshift))
	    yerr = yerr*max(1.0, abs(yshift))
	    message = 'Adjusting R23 by %3.1f sigma and O32 by %3.1f sigma worked'
	    print message%(xshift, yshift)
	    message = 'Errors on R23 and O32 have been increased by a factor of %3.1f and %3.1f'
	    print message%(max(1.0, abs(xshift)), max(1.0, abs(yshift)))
    else:
	if x > xlimit:
	    print 'R23 and O32 outside oxyab calibration limits'
	    print 'No oxygen abundance estimated'
	    return None
    if KK04:
	#oxyab, oxyaberr = oxyab_KK04_eqn18(x, y, xerr, yerr)
	#if oxyab < 8.4:
	#    print 'KK04 oxygen abundance would be < 8.4'
	#    print 'No oxygen abundance estimated'
	#    return None
        results = oxyab_KK04(x, y, xerr, yerr, branch=branch)
	if None in results:
	    return None
	else:
	    oxyab, oxyaberr = results
    else:
        if branch == 'low':
            results = oxyab_M91_low(x, y, xerr, yerr)
        else:
            results = oxyab_M91_high(x, y, xerr, yerr)
	if None in results:
	    return None
	else:
	    oxyab, oxyaberr = results
    return oxyab, oxyaberr, warning

def oxyab_KK04_eqn18(x, y, xerr=None, yerr=None):
    # Compute the oxygen abundance 12 + log(O/H)
    # using the analytical expressions of Kobulnicky & Kewley (2004).
    # Equation 18: an average of KD02 and M91
    # Upper branch only
    xterm = 9.11 - 0.218*x - 0.0587*x**2 - 0.330*x**3 - 0.199*x**4
    yterm = 0.00235 - 0.01105*x - 0.051*x**2 - 0.04085*x**3 - 0.003585*x**4
    oxyab = xterm - y * yterm
    if xerr is not None and yerr is not None:
	dxterm = -0.218 - 2*0.0587*x - 3*0.330*x**2 - 4*0.199*x**3
	dyterm = -0.01105 - 2*0.051*x - 3*0.04085*x**2 - 4*0.003585*x**3
	xtermerr2 = (xerr * (dxterm - y*dyterm))**2
	ytermerr2 = (xerr * yterm)**2
	oxyaberr = sqrt(xtermerr2 + ytermerr2)
	return oxyab, oxyaberr
    else:
	return oxyab

def oxyab_KK04(x, y, xerr=None, yerr=None, branch='high',
	       nmcerr=0, plot=False):
    # Compute the oxygen abundance 12 + log(O/H)
    # using the theoretical model of Kewley and Dopita (2002) as
    # given in the new parameterization of Kobulnicky & Kewley (2004)
    # equation 17 (upper branch) and equation 16 (lower branch).
    # As log(q) depends on oxygen abundance, must iterate to solution
    # equation 13 gives log(q) as a function of oxyab and y=log(O32)
    eps = 0.001
    low_prob_on_cal = 0.1  # must have > 10% prob of being on calibration
    high_prob_on_cal = 0.75  # above this prob assume high branch
    high = oxyab_KK04_solve(x, y, 'high')
    low = oxyab_KK04_solve(x, y, 'low')
    if None not in [high, low] and low > high:
	oxyab = None
    else:
	if branch == 'low':
	    oxyab = low
	else:
	    oxyab = high
    if xerr is not None and yerr is not None:
	if nmcerr > 0:
	    oxyab_mc_low = []
	    oxyab_mc_high = []
	    x_mc = RA.normal(x, xerr, nmcerr)
	    y_mc = RA.normal(y, yerr, nmcerr)
	    for i in range(nmcerr):
		high = oxyab_KK04_solve(x_mc[i], y_mc[i], 'high')
		low = oxyab_KK04_solve(x_mc[i], y_mc[i], 'low')
		if None in [low, high]:
		    low = 999
		    high = -999
		oxyab_mc_low.append(low)
		oxyab_mc_high.append(high)    
	    oxyab_mc_low = N.array(oxyab_mc_low)
	    oxyab_mc_high = N.array(oxyab_mc_high)
	    ok = oxyab_mc_low <= oxyab_mc_high
	    n_on_cal = N.sum(ok.astype(N.Int))
	    print 'n_on_cal = ', n_on_cal
	    prob_on_cal = float(n_on_cal)/nmcerr
	    print 'prob_on_cal = %5.3f'%prob_on_cal
	    oxyab_mc_low = N.compress(ok, oxyab_mc_low)
	    oxyab_mc_high = N.compress(ok, oxyab_mc_high)
	    x_mc = N.compress(ok, x_mc)
	    if prob_on_cal > low_prob_on_cal:
		if prob_on_cal > high_prob_on_cal:
		    oxyab_mc = oxyab_mc_high
		else:
		    oxyab_mc = N.concatenate((oxyab_mc_low, oxyab_mc_high))
		oxyab_mc = N.sort(oxyab_mc)
		nmcerrcount = len(oxyab_mc)
		low68cl = oxyab_mc[int(0.16*nmcerrcount)]
		high68cl = oxyab_mc[int(0.84*nmcerrcount)]
		oxyaberr = 0.5*(high68cl - low68cl)
		if oxyab is None:
		    oxyab = oxyab_mc[int(0.50*nmcerrcount)]
		if plot:
		    pgaqt()
		    pgsetup()
		    pgenv(7.0, 10.0, 0, 0.5*nmcerr)
		    pglab('oxyab', 'freq', '')
		    pghist_s(N.array(oxyab_mc), 100, 5, 7.0, 10.0)
		    pgend()
		    pgaqt()
		    pgsetup()
		    pgenv(0.0, 1.5, 7, 10)
		    pglab('log10(R23)', 'oxyab', '')
		    pgxpt(N.array(x_mc), oxyab_mc_high, 'dot')
		    pgxpt(N.array(x_mc), oxyab_mc_low, 'dot')
		    pgend()
	    else:
		oxyab = oxyaberr = None
	else:
	    dbydx = (oxyab_KK04_solve(x+eps, y, branch) - 
		     oxyab_KK04_solve(x-eps, y, branch)) / (2*eps)
	    dbydy = (oxyab_KK04_solve(x, y+eps, branch) - 
		     oxyab_KK04_solve(x, y-eps, branch)) / (2*eps)
	    oxyaberr = sqrt(dbydx**2 * xerr**2 + dbydy**2 * yerr**2)
	return oxyab, oxyaberr
    else:
	return oxyab

def oxyab_KK04_high(x, y, xerr=None, yerr=None):
    return oxyab_KK04(x, y, xerr, yerr, branch='high')

def oxyab_KK04_low(x, y, xerr=None, yerr=None):
    return oxyab_KK04(x, y, xerr, yerr, branch='low')

def oxyab_KK04_solve(x, y, branch):
    maxiter = 200
    precision = 0.00001
    # initial values
    logq = 7.2
    oxyab_previous = 0.0
    delta = 1
    for i in range(maxiter):
	if branch == 'high':
	    oxyab = oxyab_KK04_eqn17(x, logq)
	elif branch == 'low':
	    oxyab = oxyab_KK04_eqn16(x, logq)
	else:
	    print 'Invalid branch specifier'
	delta = abs(oxyab - oxyab_previous)
	if delta < precision: break
	oxyab_previous = oxyab
	logq = logq_KK04_eqn13(y, oxyab)
    if delta >= precision:
	print 'Warning: oxyab_KK04_solve did not converge'
	return None
    else:
	return oxyab

def oxyab_KK04_eqn17(x, logq):
    term1 = 9.72 - 0.777*x - 0.951*x**2 - 0.072*x**3 - 0.811*x**4
    term2 = 0.0737 - 0.0713*x - 0.141*x**2 + 0.0373*x**3 - 0.058*x**4
    oxyab = term1 - logq * term2
    return oxyab

def oxyab_KK04_eqn16(x, logq):
    term1 = 9.4 + 4.65*x - 3.17*x**2
    term2 = 0.272 + 0.547*x - 0.513*x**2
    oxyab = term1 - logq * term2
    return oxyab

def logq_KK04_eqn13(y, oxyab):
    term1 = 32.81 - 1.153*y**2
    term2 = -3.396 - 0.025*y + 0.1444*y**2
    term3 = 4.603 - 0.3119*y - 0.163*y**2
    term4 = -0.48 + 0.0271*y + 0.02037*y**2
    logq = (term1 + oxyab*term2)/(term3 + oxyab*term4)
    return logq

def oxyab_M91_high(x, y, xerr=None, yerr=None):
    # Compute the oxgen abundance 12 + log(O/H)
    # using the analytical expressions of McGaugh (1991, 1998)
    # as given in [K03].
    # Upper branch.
    xterm = 12 - 2.939 - 0.2*x - 0.237*x**2 - 0.305*x**3 - 0.0283*x**4
    yterm = 0.0047 - 0.0221*x - 0.102*x**2 - 0.0817*x**3 - 0.00717*x**4
    oxyab = xterm - y * yterm
    if xerr is not None and yerr is not None:
	dxterm = -0.2 - 2*0.237*x - 3*0.305*x**2 - 4*0.0283*x**3
	dyterm_by_dx = y*(-0.0221 - 2*0.102*x - 3*0.0817*x**2 - 4*0.00717*x**3)
	dyterm_by_dy = yterm
	xtermerr2 = (xerr * dxterm)**2
	ytermerr2 = (xerr * dyterm_by_dx)**2 + (yerr * dyterm_by_dy)**2
	oxyaberr = sqrt(xtermerr2 + ytermerr2)
	return oxyab, oxyaberr
    else:
	return oxyab

def oxyab_M91_low(x, y, xerr=None, yerr=None):
    # Compute the oxgen abundance 12 + log(O/H)
    # using the analytical expressions of McGaugh (1991, 1998)
    # as given in [K03].
    # Lower branch.
    xterm = 12 - 4.944 + 0.767*x + 0.602*x**2
    yterm = 0.29 + 0.332*x - 0.331*x**2
    oxyab = xterm - y * yterm
    if xerr is not None and yerr is not None:
	dxterm = 0.767 + 2*0.602*x
	dyterm_by_dx = y*(0.332 - 2*0.331*x)
	dyterm_by_dy = yterm
	xtermerr2 = (xerr * dxterm)**2
	ytermerr2 = (xerr * dyterm_by_dx)**2 + (yerr * dyterm_by_dy)**2
	oxyaberr = sqrt(xtermerr2 + ytermerr2)
	return oxyab, oxyaberr
    else:
	return oxyab

def xlimit_M91(y):
    return 0.963 + 0.140*y - 0.004*y**2

def xlimit_KK04(y):
    return 0.936 + 0.082*y + 0.006*y**2

def oxyab_calib_limit(low=oxyab_M91_low, high=oxyab_M91_high):
    pgaqt()
    pgsetup()
    pgenv(-0.5, 1.2, 7, 9.5)
    pglab('log(R\d23\u)', '12+log(O/H)', '')
    ylist = N.arange(-2.0, 2.0, 0.5)
    limits = []
    for y in ylist:
	x0 = (0.8,)
	def minfunc(x):
	    return abs(high(x[0], y) - low(x[0], y))
	xlist = N.arange(-0.5, 1.3, 0.001)
	oxyab_highlist = []
	oxyab_lowlist = []
	for x in xlist:
	    oxyab_highlist.append(high(x, y))
	    oxyab_lowlist.append(low(x, y))
	oxyab_highlist = N.array(oxyab_highlist)
	oxyab_lowlist = N.array(oxyab_lowlist)
	x = fmin(minfunc, x0, xtol=1e-8, ftol=1e-8)
	limits.append(x[0])
	print y, x, high(x, y)
	validx = xlist <= x+0.0005
	xlist = N.compress(validx, xlist)
	oxyab_highlist = N.compress(validx, oxyab_highlist)
	oxyab_lowlist = N.compress(validx, oxyab_lowlist)
	pgline(xlist, oxyab_highlist)
	pgline(xlist, oxyab_lowlist)
	pgsch(0.5*ch)
	if y == -1.5:
	    label = 'O\d32\u='
	else:
	    label = ''
	pgptxt(0.5, low(0.5, y)+0.035, 43, 1.0, label+'%3.1f'%y)
	pgsch(ch)
	#pgpt(N.array(x), N.array([high(x, y)]), pointStyles['star'])
    pgclos()
    limits = N.array(limits)
    pgaqt()
    pgsetup()
    pgenv(-2.0, 1.5, 0.5, 1.5)
    pglab('O\d32\u', 'R\d23\u limit', '')
    pgpt(ylist, limits, pointStyles['circle'])
    p = leastsq(quadratic, (1.0, 0.1, 0.0), args=(ylist, limits))
    a, b, c = map(float, p[0])
    print 'log(R23) limit = %5.3f + %5.3f * log(O32) + %5.3f * (log(O32))**2'%(a,b,c)
    limits_model = a + b*ylist + c*ylist**2
    pgline(ylist, limits_model)
    pgclos()

def oxyab_calib_plot():
    pgopen('oxyab_R23_calib.ps/cps')
    pgsetup()
    pgenv(-0.0, 1.2, 7.5, 9.5)
    pglab('log(R\d23\u)', '12+log(O/H)', '')
    # plot T04 fit
    xlist = N.arange(-0.2, 1.0, 0.001)
    yT04 = 9.185 - 0.313*xlist - 0.264*xlist**2 - 0.321*xlist**3
    pgsls(lineStyles['dotted'])
    pgsci(colourIndices['red'])
    pgslw(2*lw)
    pgline(xlist, yT04)
    pgline(N.array([0.75, 0.95]), N.array([9.325, 9.325]))
    pgsci(colourIndices['black'])
    pgslw(lw)
    pgtext(1.0, 9.3, 'T04')
    pgsci(colourIndices['blue'])
    pgsls(lineStyles['dashed'])
    pgline(N.array([0.75, 0.95]), N.array([9.175, 9.175]))
    pgsci(colourIndices['black'])
    pgtext(1.0, 9.15, 'M91')
    pgsci(colourIndices['black'])
    pgsls(lineStyles['solid'])
    pgline(N.array([0.75, 0.95]), N.array([9.025, 9.025]))
    pgtext(1.0, 9.0, 'KK04')
    ylist = N.arange(-1.0, 0.6, 0.5)
    for y in ylist:
	x0 = (0.8,)
	def minfunc(x):
	    return abs(oxyab_M91_high(x[0], y) - oxyab_M91_low(x[0], y))
	xlist = N.arange(-0.1, 1.3, 0.001)
	oxyab_highlist = []
	oxyab_lowlist = []
	for x in xlist:
	    oxyab_highlist.append(oxyab_M91_high(x, y))
	    oxyab_lowlist.append(oxyab_M91_low(x, y))
	oxyab_highlist = N.array(oxyab_highlist)
	oxyab_lowlist = N.array(oxyab_lowlist)
	x = fmin(minfunc, x0, xtol=1e-8, ftol=1e-8)
	validx = xlist <= x+0.0005
	xlist = N.compress(validx, xlist)
	oxyab_highlist = N.compress(validx, oxyab_highlist)
	oxyab_lowlist = N.compress(validx, oxyab_lowlist)
	pgsls(lineStyles['dashed'])
	pgsci(colourIndices['blue'])
	pgline(xlist, oxyab_highlist)
	pgline(xlist, oxyab_lowlist)
	pgsci(colourIndices['black'])
	pgsls(lineStyles['solid'])
	pgsch(0.75*ch)
	if y == -1.0:
	    pgptxt(1.025, 7.7+0.15, 0.0, 1.0, 'O\d32\u =')
	pgptxt(1.05, 7.7-0.15*y, 0.0, 0.0, '%+3.1f'%y)
	pgsch(ch)
	#pgpt(N.array(x), N.array([high(x, y)]), pointStyles['star'])
    for y in ylist:
	x0 = (0.8,)
	def minfunc(x):
	    return abs(oxyab_KK04(x[0], y, branch='high') - oxyab_KK04(x[0], y, branch='low'))
	xlist = N.arange(-0.1, 1.3, 0.001)
	oxyab_highlist = []
	oxyab_lowlist = []
	for x in xlist:
	    oxyab_highlist.append(oxyab_KK04(x, y, branch='high'))
	    oxyab_lowlist.append(oxyab_KK04(x, y, branch='low'))
	oxyab_highlist = N.array(oxyab_highlist)
	oxyab_lowlist = N.array(oxyab_lowlist)
	x = fmin(minfunc, x0, xtol=1e-8, ftol=1e-8)
	validx = xlist <= x+0.0005
	xlist = N.compress(validx, xlist)
	oxyab_highlist = N.compress(validx, oxyab_highlist)
	oxyab_lowlist = N.compress(validx, oxyab_lowlist)
	pgsls(lineStyles['solid'])
	pgline(xlist, oxyab_highlist)
	pgline(xlist, oxyab_lowlist)
	pgsls(lineStyles['solid'])
	#pgpt(N.array(x), N.array([high(x, y)]), pointStyles['star'])
    pgclos()


def quadratic(p, x, y):
    a, b, c = p
    return y - (a + b*x + c*x**2)

def stellar_abs_corr(EW4861):
    # Correct the EW(Hbeta) for stellar absorption,
    # as described in [KP03] and used by [K03].
    # This is simply a constant 2 Ang added to the EW.
    return EW4861[0] + 2.0, EW4861[1]
