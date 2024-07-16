import os
import exifread
from project import arg_parser, convert_latlong, write_csv, read_exif


def test_arg_parser_non():
    args = arg_parser(None)
    assert args.create == True
    assert args.view == True
    assert args.directory == "."

def test_arg_parser_v():
    args = arg_parser(["-v"])
    assert args.create == False
    assert args.view == True
    assert args.directory == "."

def test_arg_parser_c():
    args = arg_parser(["-c"])
    assert args.create == True
    assert args.view == False
    assert args.directory == "."

def test_arg_parser_cv():
    args = arg_parser(["-c", "-v"])
    assert args.create == True
    assert args.view == True
    assert args.directory == "."

def test_arg_parser_dir():
    args = arg_parser(["-c", "-v", "this is a dir/test"])
    assert args.create == True
    assert args.view == True
    assert args.directory == "this is a dir/test"
'''
class Test_class

    def __init__(self, values):
        self.values = values

obj = exifread.classes.IfdTag()

def test_convert_latlong():
    assert convert_latlong([41, 22, 11.265], 'N') == 41.36979577431396


    


def test_write_csv():
    assert write_csv()

    return
'''
    
def test_read_exif():
    assert read_exif("./templates") == []
    assert len(read_exif("./testfotos")) == 3
    assert read_exif("ioghjl_nonexisting") == []
