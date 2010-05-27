# sfr.py

# Functions for calculating SFR following
# Aragon-Salamanca et al. (2003) as in
# the thesis of Milvang-Jensen (2003).

from math import *

def LHalpha0(LOII, EWOII, MB, h50=1.4):
    # Extinction-corrected Halpha luminosity
    # as a function of [OII] luminosity, EW([OII]) and M_B
    LOII, LOII_err = LOII
    EWOII, EWOII_err = EWOII
    MB, MB_err = MB
    log_ratio = 1.40 + 0.50 * log10(EWOII) + 0.13*(MB + 5.0*log10(h50))
    log_ratio_err = sqrt( (1/(EWOII*2*log(10)))**2 * EWOII_err**2 +
                          0.13**2 * MB_err**2 )
    ratio = pow(10, log_ratio)
    ratio_err = log(10) * ratio * log_ratio_err
    LHa = LOII / ratio
    LHa_err = sqrt( (LOII_err/ratio)**2 + (ratio_err*LOII/ratio**2)**2 )
    return (LHa, LHa_err)


def SFR_Ha(LHalpha0):
    # Star-formation rate as a function of
    # extinction-corrected Halpha luminosity
    # from Kennicutt (1998)
    SFR_per_unit_L = 7.9e-42  # M_solar/year/(erg/s)
    SFR = SFR_per_unit_L * LHalpha0[0] # M_solar/year
    SFR_err = SFR_per_unit_L * LHalpha0[1] * 1.0e42
    return (SFR, SFR_err)


def SFR_OII(LOII, LOIIerr, oxyab, oxyaberr):
    # SFR (see my thesis for eqn and refs)
    # not corrected for extinction
    fOH = (-2.29*oxyab + 21.21)
    SFROII = LOII / (1.26e2 * fOH)
    SFROIIerr = SFROII * sqrt((LOII[1]/LOII[0])**2 + 
                              (2.29*oxyab[1]/fOH)**2)
    SFROII = (SFROII, SFROIIerr)

