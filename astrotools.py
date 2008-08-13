# astrotools.py

# Useful astronomy utility functions

# Steven Bamford
# Created September 2005

from math import *
import numpy as N
from ppgplot_spb import *
from cosmology import *

# convert strings of RA (hh:mm:ss.s) and Dec (dd:mm:ss.s) in to
# decimal degrees (d.ddd)
def radec_to_deg(ra, dec):
    ra_h = float(ra[: ra.find(':')])
    ra_m = float(ra[ra.find(':')+1 : ra.rfind(':')])
    ra_s = float(ra[ra.rfind(':')+1 :])
    dec_d = float(dec[: dec.find(':')])
    dec_m = float(dec[dec.find(':')+1 : dec.rfind(':')])
    dec_s = float(dec[dec.rfind(':')+1 :])
    ra_deg, dec_deg = rahms_decdms_to_deg(ra_h, ra_m, ra_s, dec_d, dec_m, dec_s)
    return ra_deg, dec_deg


def rahms_decdms_to_deg(ra_h, ra_m, ra_s, dec_d, dec_m, dec_s):
    ra_sign = (ra_h+0.5) / abs(ra_h+0.5)
    ra_h = N.absolute(ra_h)
    ra_hours = ra_sign * (ra_h + ra_m / 60.0 + ra_s / 3600.0)
    ra_deg = ra_hours * 15.0
    dec_sign = (dec_d+0.5) / abs(dec_d+0.5)
    dec_d = N.absolute(dec_d)
    dec_deg = dec_sign * (dec_d + dec_m / 60.0 + dec_s / 3600.0)
    # put onto range 0-360 deg
    if ra_deg >= 0.0:
        while ra_deg >= 360.0:  ra_deg = ra_deg - 360.0
    else:
        while ra_deg <= -360.0:  ra_deg = ra_deg + 360.0
    if dec_deg >= 0.0:
        while dec_deg >= 360.0:  dec_deg = dec_deg - 360.0
    else:
        while dec_deg <= -360.0:  dec_deg = dec_deg + 360.0
    return ra_deg, dec_deg


# calculate angle between two co-planar angles in decimal degrees
def calc_ang_diff(a1, a2):
    # Put angles on range 0 -- 360
    if a1 >= 0.0:
        while a1 >= 360.0:  a1 = a1 - 360.0
    else:
        while a1 <= -360.0:  a1 = a1 + 360.0
    if a2 >= 0.0:
        while a2 >= 360.0:  a2 = a2 - 360.0
    else:
        while a2 <= -360.0:  a2 = a2 + 360.0
    # numerical difference
    delta = a2 - a1
    # put difference on range -180 -- 180
    if delta > 180.0:
        delta = delta - 360.0
    elif delta <= -180.0:
        delta = 360.0 + delta
    return delta


def calc_ang_dist(ra1, dec1, ra2, dec2, units='degrees',
                  safe=True):
    DPIBY2 = 0.5 * pi
    
    if safe:
        ra1, dec1, ra2, dec2 = [checkarray(i, double=True)
                                for i in (ra1, dec1, ra2, dec2)]
    
    if units == "hrdeg":
        convRA = pi / 12.0
        convDEC = pi / 180.0
    elif units == "radians":
        convRA = 1.0
        convDEC = 1.0
    else:
        convRA = pi / 180.0
        convDEC = pi / 180.0
        
    theta1 = dec1*convDEC + DPIBY2
    theta2 = dec2*convDEC + DPIBY2
    cosgamma= (N.sin(theta1) * N.sin(theta2) * N.cos((ra1-ra2)*convRA) + 
               N.cos(theta1) * N.cos(theta2))
    
    adist = 0.0 * cosgamma
    ivalid = (cosgamma < 1.0).nonzero()[0]
    if len(ivalid) > 0:
        adist[ivalid] = N.arccos(cosgamma[ivalid]) / convDEC
    if adist.shape == (1,):
        return adist[0]
    else:
        return adist


def calc_ang_dist_old(ra1, dec1, ra2, dec2):
    # approx
    print 'APPROX - get djs_diff_angle from idlutils for correct calculation'
    delta_dec = dec2 - dec1
    delta_ra = (ra2 - ra1) * N.cos((pi/180)*(dec2+dec1)/2.0)
    delta = N.sqrt(delta_dec**2 + delta_ra**2)
    delta = delta * 3600.0
    return delta

def angles_to_xyz(r,phi,theta):
# Convert spherical coords (r,phi,theta) into Cartesion coords (x,y,z).

#  The angles must be in the following ranges:
#    0 <= phi < 360
#    0 <= theta <= 180
#  where theta=0 corresponds to the N pole, and theta=180 is the S pole.
#  If you want to convert from RA and DEC, pass the following
#  arguments (in degrees):  RA, 90-DEC
#  From IDLUTILS.
 
   DRADEG = 180.0/pi
   stheta = N.sin(theta / DRADEG)
   x = r * N.cos(phi / DRADEG) * stheta
   y = r * N.sin(phi / DRADEG) * stheta
   z = r * N.cos(theta / DRADEG)
 
   return x, y, z

def distance(x1, y1, z1, x2, y2, z2):
    return N.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

def _normdistance(gra, gdec, gredshift, cra, cdec, credshift, rvir, deltaz):
    # This function is not used - it has been included directly in the
    # dr6_sample.py code to speed up.
    angscale = ang_scale_flat(credshift) # kpc/arcsec
    angscale *= 3.6 # Mpc/deg
    angdist = calc_ang_dist(gra, gdec, cra, cdec) # degrees
    angdist *= angscale # Mpc
    angdist /= rvir # virial radii
    losdist = dC_flat(gredshift) - dC_flat(credshift) # Mpc
    # adjust losdist to be smaller when redshifts are similar,
    # but unchanged otherwise.
    # Fix losdist=rvir when |gredshift-credshift| < deltaz
    # and ajustment < 1 per cent for |gredshift-credshift| > 2*deltaz
    A = -N.log(1 - rvir/(dC_flat(credshift+deltaz/2.0) - dC_flat(credshift-deltaz/2.0)))
    B = N.log(N.log(100)/A)/N.log(2.0)
    C = 1 - N.exp(-A * N.abs(gredshift - credshift)**B / (deltaz**B))
    losdist *= C
    losdist /= rvir # virial radii
    dist = N.sqrt(angdist**2 + losdist**2)
    return dist

def Tfunction(p, x):
    p0, p1, q0, q1, q2 = p
    return p0 + p1*x + q0*N.tanh((x-q1)/q2)

def Tfunction04(p, x):
    p0, p1, q0, q1, q2 = p
    return p0 + p1*(x+20) + q0*N.tanh((x-q1)/q2)


def lumfn_blue_baldry04(Mr):
    # Schechter parameters for blue sequence
    #-20.90  0.00254  -0.25  0.00157  -1.54
    #  0.08  0.00032   0.23  0.00043   0.08
    pass

def lumfn_red_baldry04(Mr):
    # Schechter parameters for red sequence
    #-21.34  0.00304  -0.69  0.00000  -1.00
    #0.02  0.00008   0.02 -9.99999  -9.99
    pass

def Cur_divide_baldry06(Mstar):
    p = (2.18, 0, 0.38, 10.26, 0.85)
    return Tfunction(p, Mstar)

def Cur_divide_baldry04(Mr):
    # updated to DR4
    # http://www.astro.ljmu.ac.uk/~ikb/research/bimodality-paperI.html
    p = (2.192, 0, -0.354, -20.58, 2.05)
    return Tfunction(p, Mr)

def Cur_red_baldry04(Mr):
    # updated to DR4
    # http://www.astro.ljmu.ac.uk/~ikb/research/bimodality-paperI.html
    p = (2.386, -0.079, -0.076, -19.75, 1.04)
    # old, from paper
    #p = (2.279, -0.037, -0.108, -19.81, 0.96)
    return Tfunction04(p, Mr)

def Cur_red_baldry04_Mstar(Mstar):
    Cur = Cur_divide_baldry06(Mstar)
    deltaCur = 1.0
    oldCur = Cur 
    while deltaCur > 0.001:
        Mr = Mr_from_logMstar_baldry06(Mstar, Cur)
        Cur = Cur_red_baldry04(Mr)
        deltaCur = (N.absolute(Cur - oldCur)).max()
        oldCur = Cur
    return Mr, Cur

def Cur_blue_baldry04_Mstar(Mstar):
    Cur = Cur_divide_baldry06(Mstar)
    deltaCur = 1.0
    oldCur = Cur 
    while deltaCur > 0.001:
        Mr = Mr_from_logMstar_baldry06(Mstar, Cur)
        Cur = Cur_blue_baldry04(Mr)
        deltaCur = (N.absolute(Cur - oldCur)).max()
        oldCur = Cur
    return Mr, Cur

def Cur_sigma_red_baldry04(Mr):
    # updated to DR4
    # http://www.astro.ljmu.ac.uk/~ikb/research/bimodality-paperI.html
    p = (0.140, 0.000, 0.049, -21.23, 1.13)
    # old, from paper
    #p = (0.152, 0.008, 0.044, -19.91, 0.94)
    return Tfunction04(p, Mr)

def Cur_blue_baldry04(Mr):
    # updated to DR4
    # http://www.astro.ljmu.ac.uk/~ikb/research/bimodality-paperI.html
    p = (1.866, -0.062, -0.361, -21.29, 1.54)
    # old, from paper
    #p = (1.790, -0.053, -0.363, -20.75, 1.12)
    return Tfunction04(p, Mr)

def Cur_sigma_blue_baldry04(Mr):
    # updated to DR4
    # http://www.astro.ljmu.ac.uk/~ikb/research/bimodality-paperI.html
    p = (0.276, 0.000, -0.038, -19.88, 0.43)
    # old, from paper
    #p = (0.298, 0.014, -0.067, -19.90, 0.58)
    return Tfunction04(p, Mr)

def check_Cur_divide_baldry06():
    pgaqt()
    pgsetup()
    pgenv(8.85, 11.65, 0.0, 3.5)
    pglab('log(\(2563)/\(2563)\d\(2281)\u)', 'restframe (u-r)\dmodel\u', '')
    Mstar = N.arange(8.8, 11.8, 0.1)
    Cur = Cur_divide_baldry06(Mstar)
    pgline(Mstar, Cur)
    pgend()

def logML_baldry06(Cur):
    MLa = -0.95 + 0.56*Cur
    MLb = -0.16 + 0.18*Cur
    ML = N.where(MLa < MLb, MLa, MLb)
    return ML

def check_logML_baldry06():
    pgaqt()
    pgsetup()
    pgenv(0.5, 3.5, -1.0, 1.0)
    pglab('restframe (u-r)\dmodel\u', 'log(\(2563)/L\dr\u) (solar units)', '')
    Cur = N.arange(0.5, 3.6, 0.1)
    ML = logML_baldry06(Cur)
    pgline(Cur, ML)
    pgend()

def logMstar_baldry06(Mr, Cur):
    Mr_solar = 4.62
    logML = logML_baldry06(Cur)
    logM = (Mr_solar - Mr)/2.5 + logML
    return logM

def Mr_from_logMstar_baldry06(Mstar, Cur):
    Mr_solar = 4.62
    logML = logML_baldry06(Cur)
    Mr = Mr_solar - 2.5*(Mstar - logML)
    return Mr
