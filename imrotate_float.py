from scipy.pilutil import *
import numpy

# This is an edited version of the imrotate function
# in SciPy's pilutil.py.
# It has been changed to use a float image (rather than the default
# long integer image). Really the original function should have a mode
# parameter, but it doesn't.

def imrotate_float(arr,angle,interp='bilinear'):
    """Rotate an image counter-clockwise by angle degrees.

    Interpolation methods can be:
        'nearest' :  for nearest neighbor
        'bilinear' : for bilinear
        'cubic' or 'bicubic' : for bicubic 
    """
    func = {'nearest':0,'bilinear':2,'bicubic':3,'cubic':3}
    im = toimage(arr, mode='F')
    im = im.rotate(angle,resample=func[interp])
    return fromimage(im)
