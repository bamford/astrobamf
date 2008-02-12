import distance_modulus as dm

print 'Distance Modulus for various cosmologies and redshifts'
print '------------------------------------------------------'
print
dmods = ('z', 'Open H0=70', 'Open H0=75', 'Open H0=100',
         'Flat Std.', 'Flat WMAP1yr', 'Flat WMAP3yr', 'z')
print '%5s  %15s%15s%15s%15s%15s%15s%11s'%(dmods)

for z in [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
          1.1, 1.2, 1.3, 1.4, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0,
          6.0, 7.0, 8.0, 9.0, 10.0, 15.0, 20.0]:
    classical_70 = dm.dmod_classical(z, 70.0, 0.05)
    classical_75 = dm.dmod_classical(z, 75.0, 0.05)
    classical_100 = dm.dmod_classical(z, 100.0, 0.05)
    flat_std = dm.dmod_flat(z, 70.0, 0.3)
    flat_WMAP1 = dm.dmod_flat(z, dm.H0_WMAP1, dm.omega_m0_WMAP1)
    flat_WMAP3 = dm.dmod_flat(z, dm.H0_WMAP3, dm.omega_m0_WMAP3)
    dmods = (z, classical_70, classical_75, classical_100,
             flat_std, flat_WMAP1, flat_WMAP3, z)
    print '%7.2f%13.2f  %13.2f  %13.2f  %13.2f  %13.2f  %13.2f  %13.2f'%(dmods)
