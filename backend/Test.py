from backend.QRCodeReader import QRCodeReader

qr_code_reader = QRCodeReader("pictures/qrcodes.jpg")

print(qr_code_reader.give_box_qr_codes_and_positions())