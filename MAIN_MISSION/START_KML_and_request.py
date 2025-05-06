import subprocess
import time
import os


# Chemins absolus vers les scripts
base_dir = "/home/colin/AEAC-2025-Mission-1"
mission_dir = os.path.join(base_dir, "MAIN_MISSION")
KML_creation_script = os.path.join(mission_dir, "KML_creation.py")
request_script = os.path.join(mission_dir, "request.py")

# Lancer les scripts
KML_creation_process = subprocess.Popen(["python3", KML_creation_script])
request_process = subprocess.Popen(["python3", request_script])

print("Les deux scripts sont lancés. Entrez FIN pour les arrêter.")
entrée = "PAS FIN"
while entrée != "FIN":
    entrée = input("Entrez FIN pour arrêter les scripts : ")
    if entrée == "FIN":
        print("Arrêt des scripts...")
        break
    else:
        print("Entrée non valide. Veuillez entrer FIN pour arrêter les scripts.")

# Fermer les deux scripts
KML_creation_process.terminate()
request_process.terminate()

print("Les processus ont été arrêtés.")
