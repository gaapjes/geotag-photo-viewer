import csv
from os import path


import folium
from folium.plugins import MarkerCluster, LocateControl
from flask import Flask, cli, send_file, redirect #, render_template, request, flash, jsonify, session
from flaskwebgui import FlaskUI

# import georeader

#cli = sys.modules["flask.cli"]
cli.show_server_banner = lambda *args: None

app = Flask(__name__)
app.secret_key = "Oke Doei"

# imgdict is global dict of all image paths, used to serve the correct image
imgdict = {}


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect("/mapview")
'''
    if request.method == "POST":

        # Get button press
        if request.form.get("submit"):
            return redirect("/mapview")
    
    return render_template("index.html", map=map)
'''

@app.route("/mapview", methods=["GET", "POST"])
def mapview():
    
    # Create marker cluster
    marker_cluster = MarkerCluster(disableClusteringAtZoom=17)
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
            lat = float(row["latitude"])
            long = float(row["longitude"])
            img_path = row["path"]
            img_path = img_path.replace("\\", "/")
            imgdict[str(i)] = img_path
    
            # marker popup content, loads image url 
            img = f"<a href='/image/{i}' target='_blank'><img src='/image/{i}' title='{row['name']}' height='600px'></img></a>"
            popup = folium.Popup(img, parse_html=False, lazy=True)
            folium.Marker([lat, long], popup=popup, tooltip=row["timestamp"]).add_to(marker_cluster)

            # Focus map start viewpoint on first marker
            if i == 0:
                startpos = [lat, long]

    # Print number of images
    print("Pictures: ", len(imgdict))
    
    # Build Folium map
    map = folium.Map(location=startpos)
    LocateControl().add_to(map)
    marker_cluster.add_to(map)

    # Render map
    return map.get_root().render()
    

@app.route("/image/<id>", methods=["GET", "POST"])
def image(id):
    # Return the requested image from imgdict
    return send_file(imgdict[id])


def show_map():
    # Show in browser:
    #app.run()

    # Show in flaskwebgui window:
    ui = FlaskUI(app=app, server="flask") #, extra_flags=["--disable-sync"])
    ui.run()
    

if __name__ == "__main__":
    # Show in browser:
    app.run()
  
    # Show in flaskwebgui window:
    '''
    ui = FlaskUI(app=app, server="flask") #, extra_flags=["--disable-sync"])
    ui.run()
    '''