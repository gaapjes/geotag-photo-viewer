import csv
import exifread
import os
import sys
import argparse

def find_files(directory: str):
    #create directory tree
    return os.walk(directory)

for root, dirs, files in find_files('.'):
    print(root)



def get_gps(exif):
    try:
        geo = {"name": name, "path": img_path,
                   "latitude": convert_latlong(exif["GPS GPSLatitude"], exif['GPS GPSLatitudeRef']), "lat ref": exif['GPS GPSLatitudeRef'],
                   "longitude": convert_latlong(exif['GPS GPSLongitude'], exif['GPS GPSLongitudeRef']), "long ref": exif['GPS GPSLongitudeRef']}
    except (KeyError, ZeroDivisionError):
        #print('No geodata')
        raise
    
    # Extract Timestamp. If no timestamp, pass
    try:
        geo["timestamp"] = exif['EXIF DateTimeOriginal']
    except KeyError:
        geo["timestamp"] = ''
        pass
    return geo


def read_exif (directory: str):
    '''
    Read exif data from all files in directory\n
    :return: A List of dicts with geolocation data
    :rtype: list
    '''
    out = []

    #create directory tree
    for root, dirs, files in os.walk(directory):
        for file in files:
            img_path = os.path.abspath(os.path.join(root, file))
            # Try to read file exif
            try:
                with open(img_path, "rb") as file:
                    exif = exifread.process_file(file, details=False)
            except Exception:
                print("File read error")
                continue

            # Extract geodata converted to decimal coordinates. If no geodata, continue loop
            try:
                get_gps(exif)
            except:
                pass

            # Append geodata to output list
            out.append(geo)

    print("Geotags found:", len(out))
    return out