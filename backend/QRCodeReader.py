import cv2
from pyzbar import pyzbar

class QRCodeReader:

    def __init__(self, filename):
        self.filename = filename
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def __make_picture(self):
        ret, picture = self.cap.read()
        if not ret:
            print("No picture received.")
        else:
            cv2.imwrite(self.filename, picture)
            print(f"picture saved: {self.filename}")


    def __read_qr_codes(self, picture_path):

        picture = cv2.imread(picture_path)
        if picture is None:
            return "Path invalid"

        qr_codes = pyzbar.decode(picture)

        results = []
        for qr_code in qr_codes:
            data = qr_code.data.decode('utf-8')
            coordinates = [(point.x/2, point.y/2) for point in qr_code.polygon]
            results.append(coordinates)

        return results

    def give_box_qr_codes_and_positions(self):
        self.__make_picture()

        img = cv2.imread(self.filename)

        cropped_img = img[0:1080, 420:1500]
        cv2.imwrite(self.filename, cropped_img)

        qr_code_corners = self.__read_qr_codes(self.filename)
        final_results = []
        for qr_code in qr_code_corners:
            final_results.append(qr_code[0])
        return final_results

