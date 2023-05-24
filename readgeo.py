import csv
import exifread
import os
import sys


'''
Usage: python.exe main.py "image_folder".
Will looks for pictures in program folder when no directory specified.
exif.csv file will be saved in program folder
'''

def main(directory='.'):
    # Parse arguments, set photo directory
    # Use current directory when no argument given
    
    print(os.path.abspath(directory))


    # Set path for output file
    csv_path = "geo.csv"

    # Check if csv file, if necessary promt for write mode (Overwrite, Append, or cancel) and return write mode. Exit main() when returns False 
    mode = set_mode(csv_path)
    if not mode:
        print("Operation canceled")
        sys.exit()
    
    # Read exif data
    geodata = read_exif(directory)

    # Write csv file and print result
    if write_csv(csv_path, mode, geodata):
        print("Operation completed")
    else:
        print("No geodata found")
    return

 

# Check if csv file already exists.
# Return desired file open mode, append, overwrite, or cancel operation
def set_mode (csv_path: str):
    if not os.path.isfile(csv_path):
        return "w"
    else:
        while True:
            action = input(f"Database already exists. Do you wan to: [A]ppend, [O]verwrite, [C]ancel? : ").upper()
            if action == 'A':
                return 'a'
            elif action == 'O':
                return "w"
            elif action == 'C':
                return False



# Extract coordinates from IfdTag object and return in decimal format
def convert_latlong(latlong, ref):
    latlong = latlong.values
    # Convert degrees to decimal
    dec = latlong[0] + latlong[1] / 60 + latlong[2].decimal() / 3600
    # minus sign if ref = S or W
    dec = -1 * dec if ref.values.upper() in ('S', 'W') else dec
    return dec
  


def read_exif (directory: str):
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

            # Extract geodata converted to decimal cordinates. If no geodata, continue loop
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



# Write csv file
# On success return 'True', on failure return 'False'
def write_csv (path: str, mode: str, data: list):
    
    # Extract keys to use as header. Return 'False' if dict is empty
    try:
        header = ["name", "path", "latitude", "lat ref", "longitude", "long ref", "timestamp"]
        # header = data[0].keys()
    except IndexError:
        return False
    
    # Write csv file
    try:
        file = open(path, mode, newline='')
    except IOError:
        raise IOError

    with file:
        writer = csv.DictWriter(file, fieldnames=header)
        if mode == "w":
            writer.writeheader()
        for row in data:
            writer.writerow(row)
    
    return True

# Parses arguments and returns directory if valid directory.
# Quit program if directory invalid, return '.'' if no argment given
def parse_arg():
    if len(sys.argv) < 2:
        return '.'
    elif len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]):
            return sys.argv[1]
        else:
            sys.exit("Invalid directory")
    elif len(sys.argv) > 2:
        sys.exit("Too many arguments given")


if __name__ == "__main__":
    main(parse_arg())