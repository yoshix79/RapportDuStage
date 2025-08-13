import face_recognition
import os
import pickle
import cv2

# Dossier contenant les dossiers de visages connus
base_path = "known_faces"
known_encodings = []
known_names = []

# Parcourir chaque dossier (nom de la personne)
for person_name in os.listdir(base_path):
    person_dir = os.path.join(base_path, person_name)
    if not os.path.isdir(person_dir):
        continue

    # Parcourir les images dans le dossier
    for image_name in os.listdir(person_dir):
        image_path = os.path.join(person_dir, image_name)
        image = cv2.imread(image_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Détection et encodage
        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            known_encodings.append(encoding)
            known_names.append(person_name)

# Sauvegarder dans le fichier pickle
data = {"encodings": known_encodings, "names": known_names}
with open("encodings.pickle", "wb") as f:
    pickle.dump(data, f)

print("[INFO] Encodage terminé et enregistré dans encodings.pickle")
