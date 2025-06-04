import qrcode
import os
import uuid

def generate_qr(data):
    folder = 'app/static/qr'
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = f"{folder}/{uuid.uuid4()}.png"
    img = qrcode.make(data)
    img.save(filename)
    return filename
