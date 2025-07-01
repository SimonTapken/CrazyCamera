import cv2
from pyzbar import pyzbar

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

print("fertig")

def make_picture():
    ret, picture = cap.read()
    if not ret:
        print("No picture received.")
    else:
        filename = f"pictures/qrcodes.jpg"
        cv2.imwrite(filename, picture)
        print(f"picture saved: {filename}")


def read_qr_codes(picture_path):

    picture = cv2.imread(picture_path)
    if picture is None:
        return "Path invalid"

    qr_codes = pyzbar.decode(picture)

    results = []
    for qr_code in qr_codes:
        data = qr_code.data.decode('utf-8')
        coordinates = [(point.x, point.y) for point in qr_code.polygon]
        results.append({'data': data, 'coordinates': coordinates})

    return results

make_picture()
final_results = read_qr_codes("pictures/qrcodes.jpg")
print(final_results)