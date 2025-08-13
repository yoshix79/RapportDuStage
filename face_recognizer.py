import face_recognition
import cv2
import pickle
import datetime
import csv
import os

# Charger les encodages
with open("encodings.pickle", "rb") as f:
    data = pickle.load(f)

# Créer le fichier log si pas encore créé
log_filename = "logs.csv"
if not os.path.exists(log_filename):
    with open(log_filename, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Nom", "Date", "Heure"])

# Accès à la webcam principale (souvent index 0)
cap = cv2.VideoCapture(0)

print("[INFO] Appuyez sur 'q' pour quitter.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    for (top, right, bottom, left), face_encoding in zip(boxes, encodings):
        matches = face_recognition.compare_faces(data["encodings"], face_encoding)
        name = "Inconnu"

        face_distances = face_recognition.face_distance(data["encodings"], face_encoding)
        best_match_index = face_distances.argmin() if len(face_distances) > 0 else None

        if best_match_index is not None and matches[best_match_index]:
            name = data["names"][best_match_index]

        # Affichage rectangle et nom
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # Log dans CSV
        now = datetime.datetime.now()
        with open(log_filename, mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, now.date(), now.time()])

    cv2.imshow("Reconnaissance faciale", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
