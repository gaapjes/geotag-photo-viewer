# Exif gps extractor CS50p final project
#### Video Demo:  <URL HERE>
#### Description:

## Exif gps extractor

This program can be used to extract gps info from a folder with images containing exif date and show the images on an interactive map.

### How to use:

usage: Exif gps extractor [-h] [-c] [-v] [directory]

Will look for image files in program folder when no directory specified. geotags.csv file will be saved in program folder. By default map view will be opened    
after geodata import.

positional arguments:
  directory     Set photo directory to be read (including subdirectories)

options:
  -h, --help    show this help message and exit
  -c, --create  Only read geodata and create geotags.csv
  -v, --view    Show images from existing geotags.csv file

#### 

### Technical documentation:

The program consists of two modules: project.py an flaskviewer.py. Project.py acts as the main function and contains the logic for extracting the exif data and saving it in a .csv file. It will then call the flaskviewer.py module, which reads the geodata.csv file and spins up a local Flask server. A browser window will be opened and show a map using the 'Folium' module, with markers placed at the correct image locations. The markers can be opened to show the corresponding picture.

### project.py module functions

## arg_parser
On runtime the module parses command line arguments using python's build-in 'Argparse' module.
'--create' argument enables extracting geodata from images and creating 'geodata.csv' file.
'--view' argument enables reading 'geodata.csv' file in program root folder and showing the map view. 'Flaskviewer' module will only be imported when neccesary, to improve program startup time.
Optional image directory argument is supported, when not specified program root folder is selected (including subfolders)

## set_mode
This function will check if a geodata.csv file exists in the current directory. On finding an existing file, it will prompt the user what do do:
[A]ppend new data to the file,
[O]verwrite the file,
[S]kip the Exif read operation.

## convert_latlong
Extracted coordinates will be in 'Degrees, minutes, and seconds' format. This function will convert the coordinates to 'decimal' format as required by the folium module.

## read_exif
Uses 'argparse' module
This function will search the specified directory (including subdirectories) for all files containing exif metadata and will extract the gps coordinates.
For every file containing gpsdata a 'dict' will be created containing fields for the filename, file path, latitude and longitude.
Output is a 'list' containing the dicts.

## write_scv
Will write the list of geodata to .csv file at the specified path.
Select write_mode 'w' to overwrite existing file or create new file, or write_mode 'a' to append to existing file.

### Flaskviewer.py module functions

## route '/'
Currently a redirect to the '/mapview' route. This could in the future be used for a landing page, or possible a menu providing options.

## route '/mapview'
Reads the 'geotags.csv' in program root directory. For every line a position marker is created at the saved coordinates. Every position marker containing a popup in which the corresponding image is embedded.

## route '/image/<id>'
serves full version of the image when clicked upon.



