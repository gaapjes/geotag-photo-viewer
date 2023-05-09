import csv
import exifread
import os
import sys


'''
Usage: python.exe main.py "filepath".
Will looks for pictures in program folder when no directory specified.
exif.csv file will be saved in program folder
'''

def main():

    # Parse arguments, set photo directory
    # Use current directory when no argument given
    try:
        directory = os.path.abspath(sys.argv[1])
        if not os.path.exists(directory):
            print("Invalid directory")
            return 1
    except IndexError:
        directory = "."
   
    # Set path for output file
    csv_path = "exif.csv"

    # Create csv file and csv writer obj, exit main() when returns False 
    mode = set_mode(csv_path)
    if not mode:
        print("Operation canceled")
        return 1
    
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
        action = input(f"Database already exists. Do you wan to: [A]ppend, [O]verwrite, [C]ancel? : ").upper()

    if action == 'A':
        return "a"
    elif action == 'O':
        return "w"
    elif action == 'C':
        return False


# Extract coordinates from IfdTag and return in decimal format
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
            img_path = os.path.join(root, name)
            
            # Try to read file exif
            try:
                with open(img_path, "rb") as file:
                    exif = exifread.process_file(file, details=False)
                #print(exif)
            except Exception:
                #print("File read error")
                pass

            try:
                # Append date to exif list, geodata converted to decimal cordinates
                out.append({"path": os.path.abspath(img_path),
                           "latitude": convert_latlong(exif["GPS GPSLatitude"], exif['GPS GPSLatitudeRef']), "lat ref": exif['GPS GPSLatitudeRef'],
                           "longitude": convert_latlong(exif['GPS GPSLongitude'], exif['GPS GPSLongitudeRef']), "long ref": exif['GPS GPSLongitudeRef'],
                           "timestamp": exif['Image DateTime']})
            except KeyError:
                #print('No geodata')
                pass
    return out


# Write csv file
# On success return 'True', on failure return 'False'
def write_csv (path: str, mode: str, data: dict):
    
    # Extract keys to use as header. Return 'False' if dict is empty
    try:
        header = data[0].keys()
    except IndexError:
        return False
    
    # Write csv file
    try:
        file = open(path, mode, newline='')
    except IOError:
        raise "Unable to write csv file"

    with file:
        writer = csv.DictWriter(file, fieldnames=header)
        if mode == "w":
            writer.writeheader()
        for row in data:
            writer.writerow(row)
    
    return True


if __name__ == "__main__":
    main()