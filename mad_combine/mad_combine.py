# mad_combine.py
# PyRAF script
#
# Combines different (aligned) exposures of same observation,
# and removes cosmic rays in the process.
#
# A generalisation of EDGC/scripts/science_combine.py
#
# Steven Bamford
# Started 07-11-2003

# Refined to make more memory efficient 21-11-03.

# Note that the combined image header is a direct copy
# of the header of the first image. 

import pyfits           # provides access to fits files
import glob             # provides unix pathname matching
import os.path          # provides path operations
import numarray as num  # provides numerical array operations
import time             # provides time functions

tiny = 0.00001

# Correction factors for MAD,
# see 16-12-02.2.EDGC.log, 21-05-03.1.EDGC.log, 07-07-03.1.EDGC.log
# Dictionary - index is 'n_low,n'
# i.e. factor to multiply MAD of n_low lowest values of n by to
# get an unbiased estimator of the standard deviation
# stdev(n) = corr[n_low, n] * mad(n_low)
# The values for n_low = n aren't used here, but are left in
# for completeness and future use.
# These values were calculated using a c++ program,
# simulation_science_combine.cc
# They depend upon the read out noise, gain, background level,
# feature level and feature variability between exposures.
# If any of these are different then they need recalculating
# for the n_low and n combinations concerned.

corr = {'2,3' : 1.0/0.422,
        '4,5' : 1.0/0.562} 

# Limiting sigma for cosmic removal
sigma_limit = 5.0

# number of pixels to discard to avoid cr contamination
n_discard = 1

# The function which does the combining for each type
def mad_combine(infileglob, outfilebase):
    # get list of files to operate on
    files = glob.glob(infileglob)
    # check more than one image exists
    if files < 2:
        print 'Less than two input files found!'
        return
    print 'Operating on images',infileglob
    # get images
    images = _get_images(files)
    lenimages = len(images)
    print 'Found', lenimages, 'images'
    # get header of first image
    hdr = images[0][0].header
    # get ascard of first image
    hdrascard = hdr.ascard
    # get data from images into num (untidy tuple concatenation)
    data = num.zeros((lenimages,) + images[0][0].data.shape, num.Float32)
    for i in range(lenimages):
        data[i,:,:] = images[i][0].data
    # delete array
    del images
    # sort data
    print 'Sorting... (this may take a while, i.e an hour or so!)'
    #data_sorted = num.sort(data, axis=0)
    data_sorted = data  # for debugging
    # find standard deviation of lowest n - n_discard pixels
    print 'Calculating mad_low...'
    mad_low = _mad3(data_sorted[:-n_discard,:,:])
    # correct for bias to stddev
    num.multiply(mad_low, corr[`lenimages - n_discard` + ',' + `lenimages`], mad_low)
    # make median image
    print 'Calculating median...'
    if lenimages%2 != 0:  # then odd number of images
        m = (lenimages - 1) / 2
        median = data_sorted[m,:,:]
    else:                   # even number of images
        m = lenimages / 2
        median = (data_sorted[m,:,:] + data_sorted[m-1,:,:]) / 2
    # delete array
    del data_sorted
    # get ccd properties from header
    # these keywords are for FORS2
    # - they may need altering for other instruments

    gain = hdr['OUT1GAIN'] # N_{ADU} = gain * N_{e-}
    invgain = 1.0 / gain   # N_{e-} = invgain * N_{ADU}
    ron  = hdr['OUT1RON']  # read out noise in e- 
    # take only +ve values in median
    median_pos = num.choose(median < 0.0, (median, 0.0))
    # calculate sigma due to ccd noise for each pixel
    print 'Calculating noise_med...'
    noise_med = num.sqrt(median_pos * invgain + ron*ron) * gain
    # delete array
    del median_pos
    # find maximum of noise and mad_low
    # -> sigma to test pixels against to identify cosmics
    print 'Calculating sigma_test...'
    sigma_test = num.choose(noise_med < mad_low, (noise_med, mad_low))
    # delete arrays
    del mad_low, noise_med
    # calculate 'relative residual' for each pixel
    print 'Calculating rel_res...'
    rel_res = num.zeros(data.shape, num.Float32)
    res = num.zeros(data[0].shape, num.Float32)
    for i in range(lenimages):
        num.subtract(data[i,:,:], median, res)
        num.divide(res, sigma_test, rel_res[i,:,:])
    # delete arrays
    del sigma_test, res
    # now average over all pixels for which rel_res < sigma_limit
    # first count number included for each pixel
    # by testing to produce a boolean array, then summing over.
    print 'Calculating included...'
    included = num.zeros(rel_res[0].shape, num.Int16)
    included[:,:] = num.sum(rel_res <= sigma_limit)
    # put all discarded pixels to zero
    print 'Calculating combined...'
    pre_combine = num.choose(rel_res <= sigma_limit, (0.0,data))
    # delete array
    del rel_res
    # sum all pixels and divide by included to give mean
    combined = num.sum(pre_combine)
    # delete array
    del pre_combine
    num.divide(combined, included, combined)
    # Work out errors on this combined image
    # take only +ve values in combined
    mean_pos = num.choose(combined < 0.0, (combined, 0.0))
    # calculate sigma due to ccd noise for each pixel
    print 'Calculating noise_mean...'
    noise_mean = num.sqrt(mean_pos * invgain + ron*ron) * gain
    # delete array
    del mean_pos
    # create standard error image
    print 'Calculating error...'
    error = noise_mean / num.sqrt(included)
    # delete array
    del noise_mean
    # write all images to disk
    print 'Writing images to disk...'
    _write_images(combined, error, included,
                  hdrascard, outfilebase)


def _get_images(files):
    # return a list of image objects created from files
    images = []
    for file in files:
        image = pyfits.open(file)
        images.append(image)
    return images


# procedure to write out images
def _write_images(combined, error, included,
                  hdrascard, filebase):
    # image list
    # should be identical to argument list above, but with strings
    image_list = ['combined', 'error', 'included']
    # remove duplicated entries in header
    for j in ['SIMPLE','BITPIX','NAXIS','NAXIS1','NAXIS2']:
        del(hdrascard[j])
    for i in image_list:
        print '   -> ', i
        image_data = eval(i)
        # create new image
        image = pyfits.HDUList()
        hdu = pyfits.PrimaryHDU()
        hdu.data = image_data
        hdr = hdu.header
        hdr.ascard += hdrascard
        # add info to header
        hdr.add_history('Produced by science_combine.py ' +
                        time.strftime('%d-%m-%y-%H:%M'))
        hdr.update('PRODTYPE', i, 'type of science_combine.py product')
        # append header
        image.append(hdu)
        # save to a file
        filename = filebase + '.' + i + '.fits'
        image.writeto(filename)


# function to find standard deviation for each pixel of an array of images
# adapted from NR
# this function isn't used at the moment, but could be useful in future
def _stdev(data):
    n = len(data[:,0,0])
    s = num.zeros(data[0,:,:].shape, num.Float32)
    # First pass to get the mean.
    for j in range(n): s += data[j,:,:]
    ave = s/n
    var = num.zeros(s.shape, num.Float32)
    ep  = num.zeros(s.shape, num.Float32)
    for j in range(n):
        s = data[j,:,:]-ave
        num.add(ep, s, ep)
        p = s**2
        num.add(var, p, var)
    # Corrected two-pass formula.
    num.subtract(var, ep*ep/n, var)
    num.divide(var, (n-1), var)
    return num.sqrt(var)


def _mad3(data):
    # adapted from NR function moment
    n = len(data[:,0,0])
    s = num.zeros(data[0,:,:].shape, num.Float32)
    # First pass to get the mean.
    for j in range(n): s += data[j,:,:]
    ave = s/n
    adev = num.zeros(s.shape, num.Float32)
    for j in range(n):
        num.add(adev, num.fabs(data[j] - ave), adev)
    return adev / n


def _mad2(data, included):
    # adapted from NR function moment
    # same as mad3 but ignores zero values
    n = len(data[:,0,0])
    s = num.zeros(data[0,:,:].shape, num.Float32)
    # First pass to get the mean.
    for j in range(n): s += data[j,:,:]
    ave = s/included
    adev = num.zeros(s.shape, num.Float32)
    for j in range(n):
        d = where(num.fabs(data[j]) > tiny,
                  num.fabs(data[j] - ave),
                  0.0)
        num.add(adev, d, adev)
    return adev / included
