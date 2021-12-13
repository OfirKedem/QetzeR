import json
import math
import os
import sys
import qrcode
from pathlib import Path

class QREncoderDecoder():
    def __init__(self):
        self.id = 0

    def encode(self, data):
        if isinstance(data, str):
            data.encode('utf-8')
        encoded_data = (self.id).to_bytes(1, 'little') + data
        self.id += 1
        return encoded_data

    def decode(self, data):
        pass


def generate_qr_from_file(data, filename='example.txt', max_size=3*2**10):
    num_chunks = math.ceil(len(data) / max_size)
    qr_images = []
    qr_data = str(0) + json.dumps({'filename': filename, 'num_chunks': num_chunks})
    qr_image = qrcode.make(qr_data)
    qr_images.append(qr_image)
    for i in range(num_chunks):
        chunk = data[i * max_size:(i + 1) * max_size]
        qr_data = str(i+1) + chunk
        print(qr_data[:10])
        qr_image = qrcode.make(qr_data)
        qr_images.append(qr_image)


    return qr_images


def get_file(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    return data


if __name__ == "__main__":
    filename = Path(sys.argv[1])
    data = get_file(filename)
    imgs = generate_qr_from_file(data, filename=filename.name)

    print(len(imgs))
    for i, img in enumerate(imgs):
        path = os.path.join('./QetzeR/imgs', f'{i}.png')
        img.save(path)
# # print(qr_images)
# # for qr_image in qr_images:
# #     qr_image
# # image.show()
