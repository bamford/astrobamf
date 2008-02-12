import numpy as N

def asinh_mag_from_count_flux(count_flux, band, count_flux_err=None):
    # returns m from f/f0
    b = bsoft(band)
    m = -(2.5/N.log(10))*(N.arcsinh(count_flux/(2*b))+N.log(b))
    if count_flux_err is None:
	return m
    else:
	merr = N.absolute(-2.5 / (b * N.log(10) *
				  N.sqrt(4 + count_flux**2/b**2)) *
			   count_flux_err)
	return m, merr

def count_flux_from_observed_counts(counts, aa, kk, airmass,
				    exptime=53.907456):
    # returns f/f0
    return counts/exptime * 10**(0.4*(aa + kk * airmass))

def count_flux_from_asinh_mag(m, band, merr=None):
    # returns f/f0 from m
    b = bsoft(band)
    count_flux = N.sinh(-0.4*N.log(10) * m - N.log(b))*2*b
    if merr is None:
	return count_flux
    else:
	count_flux_err = N.absolute(N.cosh(-0.4*N.log(10) * m - N.log(b)) * 
				    -0.8*N.log(10)*b) * merr
	return count_flux, count_flux_err

def bsoft(band):
    if band == 'u':
	b = 1.4e-10
    elif band == 'g':
	b = 0.9e-10
    elif band == 'r':
	b = 1.2e-10
    elif band == 'i':
	b = 1.8e-10
    elif band == 'z':
	b = 7.4e-10
    return b

def calc_cmodel(deVMag, expMag, fracDev, band,
		deVMagErr=None, expMagErr=None):
    if deVMagErr is None or expMagErr is None:
	fdeV= count_flux_from_asinh_mag(deVMag, band=band)
	fexp = count_flux_from_asinh_mag(expMag, band=band)
	fcmodel = fracDev * fdeV + (1-fracDev) * fexp
	cmodelMag = asinh_mag_from_count_flux(fcmodel, band=band)
	return cmodelMag
    else:
	fdeV, fdeVErr = count_flux_from_asinh_mag(deVMag, merr=deVMagErr,
						  band=band)
	fexp, fexpErr = count_flux_from_asinh_mag(expMag, merr=expMagErr,
						  band=band)
	fcmodel = fracDev * fdeV + (1-fracDev) * fexp
	fcmodelErr = N.sqrt((fracDev * fdeVErr)**2 + ((1-fracDev) * fexpErr)**2)
	cmodelMag, cmodelMagErr= asinh_mag_from_count_flux(fcmodel,
					        count_flux_err=fcmodelErr,
					        band=band)
	return cmodelMag, cmodelMagErr

def test_cmodel():
    f = file('test_cmodel.dat')
    l = f.readline()
    l = f.readlines()
    f.close()
    l = [[float(e) for e in i.split(',')] for i in l]
    l = N.array(l, N.float)
    modelMag = l[:,0]
    deVMag = l[:,1]
    expMag = l[:,2]
    fracDev = l[:,3]
    lnLDeV = l[:,4]
    lnLExp = l[:,5]
    fracDevL = 1-lnLDeV/(lnLDeV+lnLExp)
    cmodelMag = calc_cmodel(deVMag, expMag, fracDev, 'r')
    cmag_corr = cmodelMag - modelMag
    for i in range(len(l)):
	print '%9.3f %9.3f %9.3f'%(modelMag[i], deVMag[i], expMag[i]),
	print '%9.3f %9.3f'%(fracDev[i], cmodelMag[i]),
	print '%9.3f'%cmag_corr[i]
