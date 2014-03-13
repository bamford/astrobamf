#! /usr/bin/env python

"""whiteboard.py - Improve a whiteboard image

    Version 2013-01-08

    Usage:
        whiteboard.py <in_image> <out_image>
    
"""

import os, sys, getopt
from scipy import misc
from scipy.ndimage import median_filter, gaussian_filter
from scipy.stats import scoreatpercentile
from scipy.interpolate import RectBivariateSpline
import numpy

def whiteboard(in_image, out_image):
    im = misc.imread(in_image)
    d = numpy.array(im)
    dtype = d.dtype
    if dtype == numpy.uint16:
        top = 2**16 - 1
    elif dtype == numpy.uint8:
        top = 2**8 - 1
    bottom = 0
    d = (top - d).astype(numpy.float)
    filtsize = (7, 7)
    bkg = numpy.zeros(d.shape, d.dtype)
    for c in range(3):
        bkgsmall = median_filter(d[::5,::5, c], filtsize, mode='nearest')
        x, y = [numpy.arange(k)*5+2.5 for k in bkgsmall.shape]
        interp = RectBivariateSpline(x, y, bkgsmall)
        xx, yy = [numpy.arange(k)+0.5 for k in d.shape[:2]]
        bkg[:,:,c] = interp(xx, yy)
    zero = d < bkg
    d -= bkg
    d[zero] = 0
    d = top - d
    low = scoreatpercentile(d.ravel(), 0.1)
    high = scoreatpercentile(d.ravel(), 50)
    d -= low
    d *= (top-bottom)/float(high-low)
    for i in range(3):
        d[:,:,i] = gaussian_filter(d[:,:,i], 1.0)
    white = d.sum(-1) > top*2.5
    d[white] = top
    for i in range(3):
        d[:,:,i] = gaussian_filter(d[:,:,i], 0.5)
    numpy.putmask(d, d>top, top)
    numpy.putmask(d, d<bottom, bottom)
    d = d.astype(dtype)
    misc.imsave(out_image, d)
    

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hf", ["help", "force"])
        except getopt.error, msg:
            raise Usage(msg)
        clobber = False
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                return 1
            if o in ("-f", "--force"):
                clobber = True
        if len(args) in (2,):
            in_image, out_image = args
            whiteboard(in_image, out_image)
        else:
            raise Usage("Wrong number of arguments")
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "For help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
