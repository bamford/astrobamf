import Image, numpy
from glob import glob

def image_changed(f1, f2):
    im1 = numpy.asarray(Image.open(f1))
    im2 = numpy.asarray(Image.open(f2))
    if im1.shape != im2.shape:
        return True
    n = numpy.product(im1.shape)
    diff = numpy.sum(numpy.absolute(im1 - im2))
    return diff > 1

def compare_directories(dir1, dir2):
    changed = []
    nomatch1 = []
    ls1 = glob(dir1+'/*')[:10]
    ls2 = glob(dir2+'/*')[:10]
    for f1 in ls1:
        f2 = f1.replace(dir1, dir2, 1)
        try:
            i = ls2.index(f2)
        except ValueError:
            nomatch1.append(f1)
        else:
            if image_changed(f1, f2):
                changed.append(f1)
            del(ls2[i])
    nomatch2 = ls2
    return changed, nomatch1, nomatch2
            
