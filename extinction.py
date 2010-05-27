# extinction.py

# Functions to calculate extinction corrections and correct line
# fluxes, etc.

import cosmology
import numpy as N
import errors

def kappa(lam):
    # The absolute extinction per unit colour excess at wavelength lam
    # for interstellar extinction law of Cardelli et al. (1989)
    # lam in Angstroms
    RV = 3.1  # kappa for V-band, as observed for Milky Way
    x = 10000.0/lam
    k = RV * cardelli_a(x) + cardelli_b(x)
    return k

def EBV(lam1, lam2, q1, q1err, q2, q2err):
    # The colour excess, E(B-V), determined from measurements of a
    # supposedly equal quantity (e.g. SFR) affected by extinction at
    # two different wavelengths.
    k1 = kappa(lam1)
    k2 = kappa(lam2)
    r, rerr = errors.divide(q2, q2err, q1, q1err)
    EBV, EBVerr = (2.5/(k1 - k2)) * errors.log10(r, rerr)
    EBV = N.maximum(0.0, EBV)
    EBVerr = N.absolute(EBVerr)
    return EBV, EBVerr

def extcorr(lam, EBV, EBVerr):
    # Return the extinction correction factor for a given wavelength
    # and E(B-V)
    k = kappa(lam)
    A = k * EBV
    Aerr = k * EBVerr
    corr, correrr = errors.pow10(0.4*A, 0.4*Aerr)
    return corr, correrr

def cardelli_a(x):
    # First term for interstellar extinction law of Cardelli et al. (1989)
    y = x - 1.82
    return (1.0 + 0.17699*y - 0.50447*y**2 - 0.02427*y**3 + 0.72085*y**4 
	    + 0.01979*y**5 - 0.77530*y**6 + 0.32999*y**7)

def cardelli_b(x):
    # Second term for interstellar extinction law of Cardelli et al. (1989)
    y = x - 1.82
    return (1.41338*y + 2.28305*y**2 + 1.07233*y**3 - 5.38434*y**4
	    - 0.62251*y**5 + 5.30260*y**6 - 2.09002*y**7)
