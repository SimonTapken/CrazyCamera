import cv2
import time

cap = cv2.VideoCapture(0)  # 0 steht für die Standardkamera

if not cap.isOpened():
    print("Kamera konnte nicht geöffnet werden.")
    exit()

try:
    while True:
        ret, picture = cap.read()
        if not ret:
            print("Kein Bild erhalten.")
            break

        # Bild speichern
        filename = f"bild_{int(time.time())}.jpg"
        cv2.imwrite(filename, picture)
        print(f"Bild gespeichert: {filename}")

        # 5 Sekunden warten
        time.sleep(5)

except KeyboardInterrupt:
    print("Abbruch durch Benutzer.")

cap.release()
cv2.destroyAllWindows()
