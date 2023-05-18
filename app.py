import csv
import folium
import readgeo
from folium.plugins import MarkerCluster, LocateControl
from flask import Flask, send_file #flash, jsonify, redirect, render_template, request, session, send_file
from os import path
from flaskwebgui import FlaskUI



app = Flask(__name__)


app.secret_key = "Oke Doei"

# Run readgeo module for current directory, if theres no geo.csv file
if not path.isfile("geo.csv"):
    readgeo.main()

# imglist is global list of all image paths, used to serve the correct image
imglist =[]


@app.route("/", methods=["GET", "POST"])
def index():
    
    global imglist

    # Create folium map and marker cluster
    map = folium.Map(location=[52, 4.9])
    LocateControl().add_to(map)
    marker_cluster = MarkerCluster(disableClusteringAtZoom=17).add_to(map)
    #disableClusteringAtZoom=14
    
    # Read geadata csv file
    try:
        file = open("geo.csv", "r")
    except IOError:
        return "No geodata file was found"
    
    # Create a marker for each picture
    with open("geo.csv", "r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            lat = row["latitude"]
            long = row["longitude"]
            img_path = row["path"]
            img_path = img_path.replace("\\", "/")

            imglist.append(img_path)
    
            # marker popup content, loads image url 
            img = f"<a href='/image/{i}' target='_blank'><img src='/image/{i}' title='{row['name']}' height='600px'></img></a>"
            
            popup = folium.Popup(img, parse_html=False, lazy=True)
            
            folium.Marker([lat, long], popup=popup, tooltip=row["timestamp"]).add_to(marker_cluster)

    # Print numer of pictures on map
    print("Pictures: ", len(imglist))
    
    # Show Folium map
    return map.get_root().render()


@app.route("/image/<int:id>", methods=["GET", "POST"])
def image(id):
    # Return the requested image from imglist
    global imglist
    return send_file(imglist[id])



if __name__ == "__main__":
  # If you are debugging you can do that in the browser:
  #app.run()
  
  # If you want to view the flaskwebgui window:
  FlaskUI(app=app, server="flask").run()