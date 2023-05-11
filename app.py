import csv
import folium
import readgeo
from folium.plugins import MarkerCluster
from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_file
from os import path
from flaskwebgui import FlaskUI


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
'''
app.config["TEMPLATES_AUTO_RELOAD"] = True
'''
'''
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
'''

app.secret_key = "Oke Doei"
#app.config['SESSION_TYPE'] = 'filesystem'

# Run readegeo module if theres no geadate csv file
if not path.isfile("geo.csv"):
    readgeo.main('.')


@app.route("/", methods=["GET", "POST"])
def index():
    # Create folium map and marker cluster
    map = folium.Map(location=[52, 4.9])
    marker_cluster = MarkerCluster(disableClusteringAtZoom=15).add_to(map)
    #disableClusteringAtZoom=13

    # Read geadata csv file and create a marker for each entry
    imglist = []
    try:
        file = open("geo.csv", "r")
    except IOError:
        return "No geodata file was found"
    
    with open("geo.csv", "r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            lat = row["latitude"]
            long = row["longitude"]
            img_path = row["path"]
            img_path = img_path.replace("\\", "/")

            imglist.append(img_path)
    
            # marker popup content
            img = f"<a href='/image/{i}' target='_blank'><img src='/image/{i}' title='{row['name']}' height='480px'></img></a>"
            
            popup = folium.Popup(img, parse_html=False)
            
            folium.Marker([lat, long], popup=popup, tooltip=row["timestamp"]).add_to(marker_cluster)

    session["imglist"] = imglist
    #folium.Marker([46.216, -124.1280], popup=htmlcode, tooltip=tooltip).add_to(map)

    return map.get_root().render()



@app.route("/image/<int:id>", methods=["GET", "POST"])
def image(id):

    return send_file(session["imglist"][id])


if __name__ == "__main__":
  # If you are debugging you can do that in the browser:
  # app.run()
  # If you want to view the flaskwebgui window:
  FlaskUI(app=app, server="flask").run()