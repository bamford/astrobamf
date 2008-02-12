import distance_modulus as dm
import math

print 'Angular scales in kpc/arcsec for various cosmologies and redshifts'
print '------------------------------------------------------------------'
print
out = ('z', 'Open H0=70', 'Open H0=75', 'Open H0=100',
       'Flat Std.', 'Flat WMAP1yr', 'Flat WMAP3yr', 'z')
print '%5s  %15s%15s%15s%15s%15s%15s%11s'%(out)

for z in [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
          1.1, 1.2, 1.3, 1.4, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0,
          6.0, 7.0, 8.0, 9.0, 10.0, 15.0, 20.0]:
    arcsec_in_rad = 180*60*60/math.pi
    kpc_in_Mpc = 10**3
    conversion = arcsec_in_rad / kpc_in_Mpc
    flat_std = dm.dA_flat(z, 70.0, 0.3) / conversion
    flat_WMAP1 = dm.dA_flat(z, dm.H0_WMAP1, dm.omega_m0_WMAP1) / conversion
    flat_WMAP3 = dm.dA_flat(z, dm.H0_WMAP3, dm.omega_m0_WMAP3) / conversion
    classical_70 = dm.dA_classical(z, 70.0, 0.05) / conversion
    classical_75 = dm.dA_classical(z, 75.0, 0.05) / conversion
    classical_100 = dm.dA_classical(z, 100.0, 0.05) / conversion
    out = (z, classical_70, classical_75, classical_100,
           flat_std, flat_WMAP1, flat_WMAP3, z)
    print '%7.2f%13.2f  %13.2f  %13.2f  %13.2f  %13.2f  %13.2f  %13.2f'%(out)
