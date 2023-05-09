import csv
import folium

from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    map = folium.Map(location=[52, 4.9])
    tooltip = "Click me!"

    with open("exif.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat = row["latitude"]
            long = row["longitude"]
            path = row["path"]

            name = path.replace("\\", "/")
            name = f"file:///{name}"

            #name = f'<a href="file:///{name}">link</a>'
            #print(name)
            popup = folium.Popup(name, parse_html=False)
            folium.Marker([lat, long], popup=popup, tooltip=tooltip).add_to(map)

    
    '''
    htmlcode = """<div>
    <img src="/img_chania.jpg" alt="Flowers in Chania" width="230" height="172">
    <br /><span>Flowers in Chania</span>
    </div>"""
    tooltip = "Click me!"

    folium.Marker([46.216, -124.1280], popup=htmlcode, tooltip=tooltip).add_to(map)
    '''


    return map.get_root().render()
    #return render_template('index.html', map=map)