import csv
import os
import sys
import argparse

import exifread
import project

def make_ratio(float):
    return exifread.utils.Ratio.from_float(float)

def make_ifdtag(longlat, ref):
    if len(longlat) != 3 or type(longlat[2]) is not exifread.utils.Ratio or type(ref) is not str:
        raise TypeError
    
    ref = ref.upper()
    if ref in ["N", "S"]:
        tag = exifread.classes.IfdTag(longlat, 2, 5, longlat, 6040, 24)
        ref = exifread.classes.IfdTag(ref, 1, 2, ref, 5948, 2)
    elif ref in ["W", "E"]:
        tag = exifread.classes.IfdTag(longlat, 4, 5, longlat, 6064, 24)
        ref = exifread.classes.IfdTag(ref, 3, 2, ref, 5972, 2)
    else:
        raise ValueError
    return tag, ref
    

#test coordinates
testlist = [
    [[42, 22, make_ratio(4.4724)], 'N'],
    [[-71, 7, make_ratio(36.4152)], 'E'],
    [[0, 0, make_ratio(0)], 'N']
]



# correct coordinates
for i in testlist:
    tag = make_ifdtag(i[0], i[1])
    out = project.convert_latlong(tag[0], tag[1])
    print(out)