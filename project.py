import csv
import exifread
import os
import sys
import argparse

from flaskviewer import show_map



'''
Usage: python.exe project.py "image_folder".
Will looks for pictures in program folder when no directory specified.
exif.csv file will be saved in program folder
'''

def main():
    '''
    Parse arguments, set photo directory. Use current directory when no argument given
    '''
    args = arg_parser()

    if args.create:
        # Give error if folder path doesn't exist
        directory = os.path.abspath(args.directory)
        print(directory)
        if not os.path.exists(directory):
            sys.exit("Invalid directory")

        # Set path for output file
        csv_path = "geotags.csv"

        # Check if csv file, if necessary promt for write mode (Overwrite, Append, or Skip) and return write mode. Exit main() when returns False 
        mode = set_mode(csv_path)
        if mode:
            # Read exif data
            geodata = read_exif(directory)
            # Write csv file
            write_csv(csv_path, mode, geodata)
            print("Geotag extraction completed") 
        else:
            # If Skip was selected
            print("Geotag extraction skipped")
    
    if args.view:
        # run the flaskwebgui window
        show_map()
    


def set_mode(csv_path: str):
    '''
    Check if csv file already exists. Return desired file open mode, append, overwrite, or cancel operation
    '''
    if not os.path.isfile(csv_path):
        return "w"
    else:
        while True:
            action = input(f"Database already exists. Do you want to: [A]ppend, [O]verwrite, [S]kip? : ").upper()
            if action == 'A':
                return 'a'
            elif action == 'O':
                return "w"
            elif action == 'S':
                return False



def convert_latlong(latlong, ref):
    '''
    Convert Latitude/Longitude valus from minutes to decimal format.\n
    :type IfdTag obj: latlong
    :return: Latitude/Longitude in decimal format
    :rtype: float
    '''
    # Extract coordinates from IfdTag object
    latlong = latlong.values
    # Convert degrees to decimal
    dec = latlong[0] + latlong[1] / 60 + latlong[2].decimal() / 3600
    # minus sign if ref = S or W
    dec = -1 * dec if ref.values.upper() in ('S', 'W') else dec
    return dec
  

def read_exif (directory: str):
    '''
    Read exif data from all files in directory\n
    :return: A List of dicts with geolocation data
    :rtype: list
    '''
    out = []

    #create directory tree
    for root, dirs, files in os.walk(directory):
        for name in files:
            img_path = os.path.abspath(os.path.join(root, name))
            # Try to read file exif
            try:
                with open(img_path, "rb") as file:
                    exif = exifread.process_file(file, details=False)
            except Exception:
                print("File read error")
                continue

            # Extract geodata converted to decimal coordinates. If no geodata, continue loop
            try:
                geo = {"name": name, "path": img_path,
                           "latitude": convert_latlong(exif["GPS GPSLatitude"], exif['GPS GPSLatitudeRef']), "lat ref": exif['GPS GPSLatitudeRef'],
                           "longitude": convert_latlong(exif['GPS GPSLongitude'], exif['GPS GPSLongitudeRef']), "long ref": exif['GPS GPSLongitudeRef']}
            except (KeyError, ZeroDivisionError):
                #print('No geodata')
                continue
            
            # Extract Timestamp. If no timestamp, pass
            try:
                geo["timestamp"] = exif['EXIF DateTimeOriginal']
            except KeyError:
                geo["timestamp"] = ''
                print("No Timestamp")
                pass

            # Append geodata to output list
            out.append(geo)

    print("Geotags found:", len(out))
    return out


def write_csv (path: str, mode: str, data: list):
    '''
    Write csv file
    On success return 'True', on failure return 'False'
    '''
    
    # Extract keys to use as header. Return 'False' if dict is empty
    '''
    try:
        header = data[0].keys()
    except IndexError:
        return False
    '''

    # Create csv file header
    header = ["name", "path", "latitude", "lat ref", "longitude", "long ref", "timestamp"]
    
    # Write csv file
    try:
        file = open(path, mode, newline='')
    except IOError:
        raise IOError("Error writing geotags.csv file")

    with file:
        writer = csv.DictWriter(file, fieldnames=header)
        if mode == "w":
            writer.writeheader()
        for row in data:
            writer.writerow(row)
    
    return True

# Parses arguments and returns directory if valid directory. 
# Quit program if directory invalid, return '.'' if no argument given
def parse_arg():
    ''' DEPRECATED '''
    if len(sys.argv) < 2:
        return '.'
    elif len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]):
            return sys.argv[1]
        else:
            sys.exit("Invalid directory")
    else: # len(sys.argv) > 2:
        sys.exit("Too many arguments given")


def arg_parser():
    '''
    Parse command line arguments
    :flag --scan: Only extract and geodata and create csv
    :flag --view: Only Load csv and view in Folium
    :arg directory: Selects picture directory
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create', action="store_true", help="Only read geodata and crate geo.csv")
    parser.add_argument('-v', '--view', action="store_true", help="Show images from existing geo.csv file")
    parser.add_argument('directory', default=".", nargs="?", help="Photo directory")
    args = parser.parse_args()
    # Default mode, When no argument given, do create and view
    if not (args.create or args.view):
        args.create = args.view = True
    return args


if __name__ == "__main__":
    main()