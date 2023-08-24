import tkinter as tk
import tkintermapview
import PIL
import csv
import project


def click(marker):
    global active_marker
    global markers

    if marker.image_hidden == True:
        # Load Image
        path = marker.path
        photo = PIL.Image.open(path, mode='r', formats=None)
        photo.thumbnail((640,480))
        out = PIL.ImageTk.PhotoImage(photo)
        marker.image = out

        # If a marker is currently active, Set image_hidden for that marker
        if active_marker:
            markers[active_marker].hide_image(True)

        # Unhide image and Mark current marker as active
        active_marker = marker.id
        marker.hide_image(False)
    
    elif marker.image_hidden == False:
        # Hide image and unset active marker
        active_marker = False
        marker.hide_image(True)
    

#project.main()

active_marker = False

# create tkinter window
root_tk = tk.Tk()
root_tk.geometry(f"{1024}x{768}")
root_tk.title("map_view_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=1024, height=768, corner_radius=0)
map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
# Use google maps
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal


# Read csv to make list of markers
markers = []
with open("geotags.csv", "r") as file:
    reader = csv.DictReader(file)
    for i, row in enumerate(reader):
        path = row["path"]
        lat = float(row["latitude"])
        long = float(row["longitude"])
        marker = map_widget.set_marker(lat, long, command=click)
        # Add id and image filepath to marker
        marker.id = i
        marker.path = row["path"]

        marker.hide_image(True)
        markers.append(marker)



root_tk.mainloop()