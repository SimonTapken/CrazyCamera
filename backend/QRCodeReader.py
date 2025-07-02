import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
from qreader import QReader
import cv2

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

        results = []
        qreader = QReader()
        qr_codes = qreader.detect_and_decode(image=picture, return_detections=True)
        content = qr_codes[0]
        position = qr_codes[1]
        for i in range(0, len(content)):
            print(f"QR-Code {i}: Inhalt: {content[i]} Position: {position[i]['cxcy']}")
            results.append((content[i], position[i]['cxcy']))

        return results

    def give_box_qr_codes_and_positions(self):
        self.__make_picture()

        img = cv2.imread(self.filename)

        cropped_img = img[0:1080, 420:1500]
        cv2.imwrite(self.filename, cropped_img)

        content_and_positions = self.__read_qr_codes(self.filename)

        final_results = []
        for content_and_position in content_and_positions:
            final_results.append((content_and_position[0], (int(content_and_position[1][0])/2, int(content_and_position[1][1])/2)))

        return final_results
