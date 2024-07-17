import csv
import exifread
import os
import sys
import argparse

print(dir(exifread.utils.Ratio))
rat = exifread.utils.Ratio()
lattag = exifread.classes.IfdTag([], 2, 5, [], 6040, 24)
lontag = exifread.classes.IfdTag([], 4, 5, [], 6064, 24)


