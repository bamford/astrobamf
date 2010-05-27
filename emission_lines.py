# emission_lines.py

# Functions to calculate line fluxes and
# luminosities, equivalent widths and magnitudes.

import cosmology
from math import *

# metres per pc:
m_per_pc = 3.0856775807e16

# in units of 10**42 erg/s/Ang
def lum_from_flux(F, z):
    # Luminosity from flux, assuming flat concordance cosmology.
    # dL = cosmology.dL_flat(z)
    dL = 10.0e-6 # 10pc in Mpc - absolute flux given (i.e. at 10pc)
    # convert from Mpc to cm
    dL = dL * 1.0e6 * m_per_pc * 1.0e2
    L = []
    for i in range(len(F)): L.append(4.0 * pi * dL**2 * F[i] * 1.0e-42)
    return tuple(L)


def F_cont_B(MB):
    # Continuum flux at effective wavelength of B-band (~4450 Ang)
    # given rest-frame B-band total magnitude, as given by
    # Fukugita et al. (1995)
    zp = 6.19e-9  # erg/s/cm**2/Ang
    MB, MB_err = MB
    F = zp * pow(10, -0.4*MB)
    F_err = log(10) * F * MB_err
    return (F, F_err)


def F_cont_OII(MB, SED, fukugita=0):
    # Continuum flux at wavelength of [OII] (3727 Ang)
    # given rest-frame B-band total magnitude, using above
    # relation for B-band continuum flux and SED
    # Use following ratios (given by thesis of Milvang-Jensen, 2003,
    # from SEDs used throughout this project, plus es0 value
    # measured by myself).
    if fukugita:
        # Subaru SED types, and roughly converted to EDGC scale:
        # 0  = E, 1  = S0, 2  = Sa, 3  = Sb, 4  = Sc, 5  = Sd, 6  = Im
        # 0.0= E, 0.3= S0, 0.8= Sa, 1.5= Sb, 2.5= Sc, 3.5= Sd, 4.0= Im
        # Approximate conversion from Osamu's SED numbering scheme to mine:
        print 'Osamu sedT: %4.2f,    '%SED,
        SED = min((SED/2.3)**1.6, 4.0)
        print 'My sedT: %4.2f'%SED
        # gives:
        # 0.0= E, 0.3= S0, 0.8= Sa, 1.5= Sb, 2.4= Sc, 3.5= Sd, 4.0= Im
        # Just use same flux ratios, from Coleman et al. 1980
        ratios = [0.45, 0.53, 0.67, 0.74, 0.83]
    else:
        # EDGC SED types:
        # 0 = es0, 1 = sab, 2 = sbc, 3 = scd, 4 = sdm
        ratios = [0.45, 0.53, 0.67, 0.74, 0.83]
    intSED = int(SED)
    fracSED = SED - intSED
    if fracSED < 0.01:
        ratio = ratios[intSED]
    else:
        slope = ratios[intSED+1] - ratios[intSED]
        ratio = ratios[intSED] + slope * fracSED
    flux_cont_B = F_cont_B(MB)
    flux_cont_OII = []
    for i in range(len(flux_cont_B)):
        flux_cont_OII.append(flux_cont_B[i] * ratio)
    return tuple(flux_cont_OII)


def OII_flux_from_ew(EW, MB, SED, fukugita=0):
    # Compute the flux of [OII] from it's equivalent width,
    # assuming above function for the B-band continuum
    # flux and it's relation to the continuum flux at
    # the position of [OII]
    flux_cont_OII = F_cont_OII(MB, SED, fukugita)
    EW, EW_err = EW
    flux_cont, flux_cont_err = flux_cont_OII
    flux = EW * flux_cont  # erg/s/cm**2/Ang
    flux_err = sqrt( (flux_cont*EW_err)**2 + (EW*flux_cont_err)**2)
    return (flux, flux_err)


def Halpha_flux_from_ew(EW, MB, SED):
    # Compute the flux of Halpha from it's equivalent width
    flux_cont_Halpha = F_cont_Halpha(MB, SED)
    EW, EW_err = EW
    flux_cont, flux_cont_err = flux_cont_Halpha
    flux = EW * flux_cont  # erg/s/cm**2/Ang
    flux_err = sqrt( (flux_cont*EW_err)**2 + (EW*flux_cont_err)**2)
    return (flux, flux_err)
