import cv2
from pyzbar import pyzbar

class QRCodeReader:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def __make_picture(self):
        ret, picture = self.cap.read()
        if not ret:
            print("No picture received.")
        else:
            filename = f"pictures/qrcodes.jpg"
            cv2.imwrite(filename, picture)
            print(f"picture saved: {filename}")


    def __read_qr_codes(self, picture_path):

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

    def give_box_qr_codes_and_positions(self):
        self.__make_picture()
        final_results = self.__read_qr_codes("pictures/qrcodes.jpg")
        return final_results

