import simplekml
import os
import csv

csv_path = '/home/colin/AEAC-2025-Mission-1/MAIN_MISSION/gps.csv'
liste_stock_centroids = []

with open(csv_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
        if len(row) >= 2:  # Make sure there are enough columns
            try:
                lat = float(row[0])
                lon = float(row[1])
                liste_stock_centroids.append((lat, lon))
            except ValueError:
                print(f"Warning: invalid row {row}")

kml = simplekml.Kml()

nombre_hotspots = 0
for lat, lon in liste_stock_centroids:
    nombre_hotspots += 1
    name_point = f"Hotspot {nombre_hotspots}"
    point = kml.newpoint(name=name_point, coords=[(lon, lat)])  # KML uses (longitude, latitude)

kml.save(os.path.join(os.path.dirname(csv_path), 'Latest.kml'))

