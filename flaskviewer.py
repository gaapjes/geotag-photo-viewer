import csv
import folium
from folium.plugins import MarkerCluster, LocateControl
from flask import Flask, cli, send_file, render_template, request, redirect #flash, jsonify, ,  , session
from os import path
from flaskwebgui import FlaskUI

# import georeader

#cli = sys.modules["flask.cli"]
cli.show_server_banner = lambda *args: None

app = Flask(__name__)
app.secret_key = "Oke Doei"
ui = FlaskUI(app=app, server="flask")

# Run readgeo module for current directory, if theres no geotags.csv file
'''
if not path.isfile("geotags.csv"):
    readgeo.main('.')
'''

# imglist is global list of all image paths, used to serve the correct image
#imglist = []
imgdict = {}


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect("/mapview")
    if request.method == "POST":

        # Get button press
        if request.form.get("submit"):
            return redirect("/mapview")
    

    return render_template("index.html", map=map)


@app.route("/mapview", methods=["GET", "POST"])
def mapview():
    
    global imglist

    # Create folium map and marker cluster
    map = folium.Map(location=[52, 4.9])
    LocateControl().add_to(map)
    marker_cluster = MarkerCluster(disableClusteringAtZoom=17).add_to(map)
    #disableClusteringAtZoom=14
    
    # Read geadata csv file
    try:
        file = open("geotags.csv", "r")
    except IOError:
        return "No geodata file was found"
    
    # Create a marker for each picture
    with open("geotags.csv", "r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            lat = row["latitude"]
            long = row["longitude"]
            img_path = row["path"]
            img_path = img_path.replace("\\", "/")

            #imglist.append(img_path)
            imgdict[str(i)] = img_path
    
            # marker popup content, loads image url 
            img = f"<a href='/image/{i}' target='_blank'><img src='/image/{i}' title='{row['name']}' height='600px'></img></a>"
            
            popup = folium.Popup(img, parse_html=False, lazy=True)
            
            folium.Marker([lat, long], popup=popup, tooltip=row["timestamp"]).add_to(marker_cluster)

    # Print numer of pictures on map
    print("Pictures: ", len(imgdict))
    
    # Show Folium map
    return map.get_root().render()


'''
@app.route("/image/<int:id>", methods=["GET", "POST"])
def image(id):
    # Return the requested image from imglist
    global imglist
    return send_file(imglist[id])
'''
@app.route("/image/<id>", methods=["GET", "POST"])
def image(id):
    # Return the requested image from imglist
    global imgdict
    return send_file(imgdict[id])


def show_map():
    ui.run()


if __name__ == "__main__":
    ui.run()

    # If you are debugging you can do that in the browser:
    #app.run()
  
    # If you want to view the flaskwebgui window:
    #FlaskUI(app=app, server="flask").run()


