import csv
import os
import simplekml
from time import sleep
import datetime as dt
import math

chemin_mission_1 = "/home/colin/AEAC-2025-Mission-1/"
main_path = os.path.join(chemin_mission_1, "MAIN_MISSION")
csv_path = os.path.join(main_path, "csvs")
kml_path = os.path.join(main_path, "KMLS")

'''
Input du code suivant :
fichiers 'stock_source_feu' & 'stock_centroids'

Output du code suivant :
Création d'un fichier KML adapté aux requis de la compé.
Le KML contient l'analyse des hotspots et de la source du feu.

Date dernière itération : 2 avril 2025
Auteur : Laurent Ducharme
'''


#from helper_funcs import haversine #pas nécessaire, la fct haversine est de la ligne 19 à 31 pour l'instant


def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))


liste_verif_stock_centroids = []
source_feu = []


#Fin du : À commenter

while True:
    try:
        print("Source of fire file exists, opening it...")
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                source_feu = row
        break
    except:
        print("Source of fire file not found, trying again later...")
        sleep(5)
        continue


source_feu_coord = (source_feu[0], source_feu[1])

version_KML = 1

while True :
    liste_stock_centroids = []

    file_path = os.path.join(csv_path, 'stock_centroids')
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            liste_stock_centroids.append(tuple(row))
    #print(liste_stock_centroids)
    
    presumed_new_gps_coords = [point for point in liste_stock_centroids if point not in liste_verif_stock_centroids]
    #print(presumed_new_gps_coords)

    if presumed_new_gps_coords == []:
        print(f"==> Version {version_KML} du KML pas encore effectuée. Aucun nouveau point pour l'instant ({dt.datetime.now()}).")
        sleep(5)
        continue

    new_gps_coords = []
    liste_gps_remove = []

    if liste_verif_stock_centroids == []:
        new_gps_coords = presumed_new_gps_coords

    else:
        for gps_coord in presumed_new_gps_coords:
            for valid_centroid in liste_verif_stock_centroids:
                if haversine(gps_coord, valid_centroid) > 12:  #( haversine > tolérance en mètre), sujet à changement selon tests
                    new_gps_coords.append(gps_coord)


                """ L'anlayse de cluster rejoint les points normalement proches,
                    Donc, ce scénario ne devrait pas arriver, pas un mauvais check par exemple! 
                    À tester que les fonctions haversine marchent bien comme prévue, sinon utilser geopy pour les transformations"""
                if haversine(gps_coord, valid_centroid) < 4:   #prends moy. entre 2 pnts gps proches (si haversine < X mètres, jugé assez proche donc)
                    lat1, lon1 = gps_coord
                    lat2, lon2 = valid_centroid
                    moy_gps = ((lat1+lat2)/2, (lon1+lon2)/2)
                    new_gps_coords.append(moy_gps)
                    liste_gps_remove.append(valid_centroid)
    
    liste_verif_stock_centroids = [gps_point for gps_point in liste_verif_stock_centroids if gps_point not in liste_gps_remove]
    
    liste_KML_ssource = liste_verif_stock_centroids + new_gps_coords

    kml = simplekml.Kml()

    lat, lon = source_feu_coord
    description_point = source_feu[2]
    point = kml.newpoint(name="Source", coords=[(lon, lat)])  # KML utilise (longitude, latitude)
    point.description = f"<![CDATA[<b>{description_point}</b>]]>"
    
    #print(liste_KML_ssource)
    
    nombre_hotspots = 0
    for coord in liste_KML_ssource:
        nombre_hotspots += 1
        lat, lon = coord
        name_point = f"Hotspot {nombre_hotspots}"
        point = kml.newpoint(name=name_point, coords=[(lon, lat)])  # KML utilise (longitude, latitude)

    nom_fichier_KML = f"{nombre_hotspots} hotspots - version {version_KML} - Équipe Zenith - Polytechnique Montréal - {dt.datetime.now()}.kml"

    version_KML += 1

    output_path = os.path.join(kml_path, nom_fichier_KML)
    kml.save(output_path)
    print(f"Fichier KML ({nom_fichier_KML}) créé ici à {dt.datetime.now()} : {output_path}")


    liste_verif_stock_centroids = liste_KML_ssource

    sleep(5)



#À commenter dès que "stock_source_feu" et "stock_centroids" sont créés
'''
sourcefeudesc = [45.5100002,-73.6204909,"Sam Chicotte"]

output_dir = "companion_computer"
file_path = os.path.join(output_dir, 'stock_source_feu')

with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(sourcefeudesc)


###

output_dir = "downloaded_files"
file_path = os.path.join(output_dir, 'stock_centroids')

with open(file_path, 'w', newline='', encoding='utf-8') as file:
    #
'''