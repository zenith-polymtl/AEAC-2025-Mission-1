import subprocess
import time
import os


# Chemins absolus vers les scripts
base_dir = "/home/avatar/companion_computer"
KML_creation_script = os.path.join(base_dir, "KML_creation.py")
request_script = os.path.join(base_dir, "request.py")

# Lancer les scripts
KML_creation_process = subprocess.Popen(["python3", KML_creation_script])
request_process = subprocess.Popen(["python3", request_script])



print("Les deux scripts sont lancés. Appuie sur Entrée pour les arrêter.")
input()

# Fermer les deux scripts
KML_creation_process.terminate()
request_process.terminate()

print("Les processus ont été arrêtés.")
