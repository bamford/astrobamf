from ppgplot_spb import *
import numpy as N
from math import sqrt, log10

def quick_plot(name, x, y, xtitle='', ytitle='',
	       xmin=None, xmax=None, xstep=None,
	       ymin=None, ymax=None, ystep=None,
	       points=False, grayscale=True, contour=False,
	       outlier_points=False, contour_labels=False,
	       cstart=2, cfactor=sqrt(2.0),
	       table='bgyrw', ramp='gamma',
	       cm_lines=False,
	       n_per_smooth_fwhm=500,
	       mean_density=50,
	       completeness=None,
	       smoothing='none'):
    print '-'*70
    print 'Plotting %s versus %s'%(ytitle, xtitle)
    print 'in file:', name
    pgopen(name+'/cps')
    pgsetup()
    n = len(x)
    if xmin is None or xmax is None:
	# just sample 10000 points to get min, max stats
	xsorted = N.sort(x[::max(1,n/10000)])
	xrange = abs(xsorted[-1] - xsorted[0])
    if xmin is None:
	xmin = xsorted[0] - 0.1*xrange
    if xmax is None:
	xmax = xsorted[-1] + 0.1*xrange
    if ymin is None or ymax is None:
	# just sample 10000 points to get min, max stats
	ysorted = N.sort(y[::max(1,n/10000)])
	yrange = abs(ysorted[-1] - ysorted[0])
    if ymin is None:
	ymin = ysorted[0] - 0.1*yrange
    if ymax is None:
	ymax = ysorted[-1] + 0.1*yrange
    pgenv(xmin, xmax, ymin, ymax, -2)
    pglab(xtitle, ytitle, '')
    if grayscale or contour:
	if smoothing == 'adaptive':
	    mean_density /= 100.0
	elif smoothing == 'basic':
	    mean_density /= 100.0
	if xstep is None:
	    nxbin = int(sqrt(float(n)/mean_density))
	else:
	    nxbin = int((xmax-xmin)/xstep)
	xstep = float(xmax-xmin)/nxbin
	if ystep is None:
	    nybin = int(sqrt(float(n)/mean_density))
	else:
	    nybin = int((ymax-ymin)/ystep)	    
	ystep = float(ymax-ymin)/nybin
	print 'nbin = %ix%i'%(nxbin, nybin)
	print 'xstep = %5.3f,  ystep = %5.3f'%(xstep, ystep)
	if smoothing == 'none':
	    xbin, ybin, dbin = bin_array_2d(x, y, 
					    nxbin, xmin, xmax,
					    nybin, ymin, ymax,
					    completeness=completeness)
	elif smoothing == 'basic':
	    smooth_fwhm = 10
	    xbin, ybin, dbin = bin_array_2d_smooth(x, y,
						   nxbin, xmin, xmax,
						   nybin, ymin, ymax,
						   smooth_fwhm,
						   completeness=completeness)
	elif smoothing == 'adaptive':
	    bin2d = bin_array_2d_super_smooth(x, y,
					      nxbin, xmin, xmax,
					      nybin, ymin, ymax,
					      n_per_smooth_fwhm,
					      completeness=completeness)
	    xbin, ybin, dbin, smooth_fwhm_min, smooth_fwhm_max = bin2d
	# Contours are spaced such that the number of galaxies
	# in a bin on the contour increases by a factor cfactor each level,
	# from at least 10 galaxies per bin, to the level below the maximum.
	# Then rescaled so that the next contour would be the
	# level of the maximum bin.
	N.putmask(dbin, dbin < 1, 10**-6)
	dbin = N.log10(dbin**(1.0/log10(cfactor)))
	dsorted = N.sort(N.ravel(dbin))
	dmax = dsorted[-1]
	print 'dmax:', (10**dmax)**(log10(cfactor))
    if grayscale:
	#pgscr(1, 0.0, 0.0, 0.5)  # makes grayscale into bluescale
	#pggray_s(dbin, dmax, dmax/10., xmin, ymin, xmax, ymax)
	setup_colour_table(table, ramp,
			   contra=1, bright=0.5,
			   flip_colours=False)
	pgimag_s(dbin, dmax, 0,
		 xmin, ymin, xmax, ymax)
	xwidth = xmax - xmin
	ywidth = ymax - ymin
	pgsci(colourIndices['white'])
	if smoothing == 'adaptive':
	    draw_circle(xmax-smooth_fwhm_max*xstep,
			ymin+smooth_fwhm_max*ystep,
			xstep, ystep, smooth_fwhm_min)
	    draw_circle(xmax-smooth_fwhm_max*xstep,
			ymin+smooth_fwhm_max*ystep,
			xstep, ystep, smooth_fwhm_max)
	elif smoothing == 'basic':
	    draw_circle(xmax-xstep*smooth_fwhm,
			ymin+ystep*smooth_fwhm,
			xstep, ystep, smooth_fwhm)
	pgsci(colourIndices['black'])
	#pgscr(1, 0.0, 0.0, 0.0)
    if contour:
	contours = 1.0*N.arange(log10(cstart**(1.0/log10(cfactor))),
				int(dmax)+1)
	contours = contours + ((dmax-1) - contours[-1])
	ncon = len(contours)
	print 'contours:', (10**contours)**(log10(cfactor))
	if grayscale:
	    pgsci(colourIndices['white'])
	pgcont_s(dbin, ncon, contours)
	if grayscale:
	    pgsci(colourIndices['black'])
	if contour_labels:
	    for c in contours[::2]:
		pgsch(ch*0.4)
		pgconl_s(dbin, c, '%i'%round((10**c)**(log10(cfactor))),
			 int(50/mean_density))
		pgsch(ch)
    if points:
	if grayscale:
	    pgsci(colourIndices['white'])
	pgpt(x, y, pointStyles['point'])
	if grayscale:
	    pgsci(colourIndices['black'])
    if outlier_points:
	xout, yout = find_outliers(dbin, nxbin, nybin, x, y, n,
				   xmin, ymin, xstep, ystep, contours[0])
	if grayscale:
	    pgsci(colourIndices['white'])
	pgpt(xout, yout, pointStyles['point'])
	if grayscale:
	    pgsci(colourIndices['black'])
    if cm_lines:
	if grayscale:
	    pgsci(colourIndices['white'])
	pgsls(lineStyles['dotted'])
	plot_baldry_cm()
	pgsls(lineStyles['solid'])
	if grayscale:
	    pgsci(colourIndices['black'])
    pgbox('BCNST', 0, 0, 'BCNST', 0, 0) 
    pgclos()


def find_outliers(dbin, nxbin, nybin, x, y, n,
		  xlow, ylow, xstep, ystep, low_contour):
    low_bin = dbin < low_contour
    outlier = N.zeros(n, N.bool)
    for k in range(n):
	jbin_index = int((x[k] - xlow)/xstep)
	ibin_index = int((y[k] - ylow)/ystep)
	if 0 <= jbin_index < nxbin and 0 <= ibin_index < nybin:
	    if low_bin[ibin_index, jbin_index]:
		outlier[k] = True
    xout = N.compress(outlier, x)
    yout = N.compress(outlier, y)
    return xout, yout


def plot_baldry_cm():
    xr = N.arange(11)/10.0 * -7 - 16.5
    yr = T_function(xr, 2.279, -0.037, -0.108, -19.81, 0.96)
    pgline(xr, yr)
    xb = N.arange(11)/10.0 * -7 - 15.5
    yb = T_function(xb, 1.790, -0.053, -0.363, -20.75, 1.12)
    pgline(xb, yb)

def T_function(x, p0, p1, q0, q1, q2):
    return p0 + p1*(x+20) + q0 * N.tanh((x-q1)/q2)
