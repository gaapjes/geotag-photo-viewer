import csv
import os
import sys
import argparse

import exifread

'''
Usage: python.exe project.py "image_folder".
Will looks for pictures in program folder when no directory specified.
geotags.csv file will be saved in program folder
'''

def main():
    '''
    Parse arguments, set photo directory. Use current directory when no argument given
    '''
    args = arg_parser(sys.argv[1:])

    if args.read:
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
            print("Geotags saved") 
        else:
            # If Skip was selected
            print("Geotags not saved")
    
    if args.view:
        # run the flaskviewer window. Import placed here to improve program startup time
        from flaskviewer import show_map
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
    #print(ref.printable, ref.tag, ref.field_type, ref.values, ref.field_offset, ref.field_length)
    #print(latlong.printable, latlong.tag, latlong.field_type, latlong.values, latlong.field_offset, latlong.field_length)
    latlong = latlong.values
    # Convert degrees to decimal
    if latlong[0] >= 0:
        dec = latlong[0] + latlong[1] / 60 + latlong[2].decimal() / 3600
    else:
        dec = latlong[0] - latlong[1] / 60 - latlong[2].decimal() / 3600

    if ref.values.upper() in ('N', 'E'):
        # dec = dec
        pass
    elif ref.values.upper() in ('S', 'W'):
        dec = -1 * dec
    else:
        raise TypeError
    
    return round(dec, 5)
  

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
                with open(img_path, "rb") as handle:
                    exif = exifread.process_file(handle, details=False)
            except Exception:
                print("File read error")
                continue

            # Extract geodata converted to decimal coordinates. If no geodata, continue loop
            try:
                geo = {"name": file, "path": img_path,
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
                pass

            # Append geodata to output list
            out.append(geo)

    print("Geotags found:", len(out))
    return out


def write_csv (path: str, write_mode: str, data: list):
    '''
    Write csv file
    On succes return 'True'
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
    
    if not write_mode in ("w", "a"):
        raise IOError(f"Incorrect write mode specified. Please use 'w' or 'a'")

    # Write csv file
    try:
        file = open(path, write_mode, newline='')
    except IOError:
        raise IOError("Error writing geotags.csv file")

    with file:
        writer = csv.DictWriter(file, fieldnames=header)
        if write_mode == "w":
            writer.writeheader()
        for row in data:
            writer.writerow(row)
    
    return True


def arg_parser(args):
    '''
    Parse command line arguments
    :flag --create: Only extract geodata and create csv
    :flag --view: Only Load csv and view in Folium
    :arg directory: Selects picture directory
    '''
    parser = argparse.ArgumentParser(
                    prog="project.py",
                    description="""Will look for image files in program folder when no directory specified.\n
                                geotags.csv file will be saved in program folder.\n
                                By default map view will be opened after geodata import.
                                """,
                    epilog="Kasper Vloon, 2024")
    parser.add_argument('-r', '--read', action="store_true", help="Only read geodata and create geotags.csv")
    parser.add_argument('-v', '--view', action="store_true", help="Show images from existing geotags.csv file")
    parser.add_argument('directory', default=".", nargs="?", help="Set photo directory to be read (including subdirectories)")
    args = parser.parse_args(args)
    # Default mode, When no argument given, do create and view
    if not (args.read or args.view):
        args.read = args.view = True
    return args


if __name__ == "__main__":
    main()