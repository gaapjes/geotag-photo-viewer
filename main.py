import csv
import os
import sys
#from pathlib import Path, WindowsPath, PureWindowsPath
import exifread



def main():

    # Set photo directory
    try:
        directory = os.path.abspath(sys.argv[1])
        if not os.path.exists(directory):
            print("Invalid path")
            return 1
    except IndexError:
        directory = "."
   

    db = []
    csv_path = "exif.csv"
    header = ["path", "latitude", "lat ref", "longitude", "long ref", "timestamp"]



    # Create csv file and csv writer obj, exit main() when returns False 
    mode = set_mode(csv_path)
    if not mode:
        print("Operation canceled")
        return 1
    

    # Read directory structure
    for root, dirs, files in os.walk(directory):
        for name in files:
            img_path = os.path.join(root, name)
            
            # Try to read file exif
            try:
                with open(img_path, "rb") as file:
                    exif = exifread.process_file(file, details=False)
                #print(exif)
            except:
                print("File error")


            try:
                #print(convert_latlong(exif["GPS GPSLatitude"]))
                db.append({"path": os.path.abspath(img_path),
                           "latitude": convert_latlong(exif["GPS GPSLatitude"], exif['GPS GPSLatitudeRef']), "lat ref": exif['GPS GPSLatitudeRef'],
                           "longitude": convert_latlong(exif['GPS GPSLongitude'], exif['GPS GPSLongitudeRef']), "long ref": exif['GPS GPSLongitudeRef'],
                           "timestamp": exif['Image DateTime']})
                #writer.writerow([path, gps["lat"], gps["long"], gps["time"]])
            except KeyError:
                #print('No GPS data')
                pass
        

    
    # Write csv file
    #header = db[0].keys()
    with open(csv_path, mode, newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        if mode == "w":
            writer.writeheader()

        for row in db:
            writer.writerow(row)

    
# Check if csv file already exists, if yes prompt user to append, overwrite, or cancel
def set_mode (csv_path):
    if not os.path.isfile(csv_path):
        return "w"
    else:
        action = input(f"Database already exists. Do you wan to: [A]ppend, [O]verwrite, [C]ancel? : ").upper()

    if action == 'A':
        return "a"
        #return open("exif.csv", "a", newline='')
    elif action == 'O':
        return "w"
        #return open("exif.csv", "w", newline='')
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
  



if __name__ == "__main__":
    main()