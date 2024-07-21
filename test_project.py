import os
import pytest

import exifread
from project import arg_parser, read_exif, convert_latlong


def test_arg_parser_non():
    args = arg_parser(None)
    assert args.read == True
    assert args.view == True
    assert args.directory == "."

def test_arg_parser_v():
    args = arg_parser(["-v"])
    assert args.read == False
    assert args.view == True
    assert args.directory == "."

def test_arg_parser_c():
    args = arg_parser(["-r"])
    assert args.read == True
    assert args.view == False
    assert args.directory == "."

def test_arg_parser_cv():
    args = arg_parser(["-r", "-v"])
    assert args.read == True
    assert args.view == True
    assert args.directory == "."

def test_arg_parser_dir():
    args = arg_parser(["-r", "-v", "/this is a dir/test"])
    assert args.read == True
    assert args.view == True
    assert args.directory == "/this is a dir/test"

    
def test_read_exif():
    assert len(read_exif(".")) == 3
    assert len(read_exif("./test images")) == 3
    assert read_exif("./templates") == []
    assert read_exif("ioghjl_nonexisting") == []



# functions to create test coordinates
def make_ratio(float):
    return exifread.utils.Ratio.from_float(float)

def make_ifdtag(longlat, ref):
    if len(longlat) != 3 or type(longlat[2]) is not exifread.utils.Ratio or type(ref) is not str:
        raise TypeError
    
    if ref.upper() in ["N", "S"]:
        tag = exifread.classes.IfdTag(longlat, 2, 5, longlat, 6040, 24)
        ref = exifread.classes.IfdTag(ref, 1, 2, ref, 5948, 2)
    elif ref.upper() in ["W", "E"]:
        tag = exifread.classes.IfdTag(longlat, 4, 5, longlat, 6064, 24)
        ref = exifread.classes.IfdTag(ref, 3, 2, ref, 5972, 2)
    else:
        tag = exifread.classes.IfdTag(longlat, 2, 5, longlat, 6040, 24)
        ref = exifread.classes.IfdTag(ref, 1, 2, ref, 5948, 2)
    return tag, ref
    

# List of test coordinates
testlist = [
    [[42, 22, make_ratio(4.4724)], 'N'],
    [[-42, 22, make_ratio(4.4724)], 'S'],
    [[-71, 7, make_ratio(36.4152)], 'E'],
    [[13, 9, make_ratio(51.919)], 'S'],
    [[72, 32, make_ratio(42.306)], 'E'],
    [[0, 0, make_ratio(0)], 'W'],
    [[1, 0, make_ratio(0)], 'n'],
    [[1, 0, make_ratio(0)], 's'],
    [[1, 0, make_ratio(0)], 'w'],
    [[1, 0, make_ratio(0)], 'e'],
]

resultlist = [42.367909,
              42.367909,
              -71.12678199999999,
              -13.1644219,
              72.545085,
              0,
              1,
              -1,
              -1,
              1,        
]

# Test convert_latlong function with list of test coordinates
def test_convert_latlong_valid():
    for i, test in enumerate(testlist):
        tags = make_ifdtag(test[0], test[1])
        print(convert_latlong(tags[0], tags[1]))
        assert abs(convert_latlong(tags[0], tags[1]) - round(resultlist[i], 6)) <= 0.000001

def test_convert_latlong_invalid():
    tags = make_ifdtag([0, 0, make_ratio(0)], "")
    with pytest.raises(TypeError):
        convert_latlong(tags[0], tags[1])

    tags = make_ifdtag([0, 0, make_ratio(0)], "Q")
    with pytest.raises(TypeError):
        convert_latlong(tags[0], tags[1])