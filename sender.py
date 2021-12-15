import json
import math
import os
import sys
from pathlib import Path

import qrcode
import base64
import imageio


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


def generate_qr_from_file(data: bytes, filename='example.txt', max_size=2 ** 10):
    num_chunks = math.ceil(len(data) / max_size)
    qr_images = []
    qr_data = base64.b64encode(
        (0).to_bytes(1, 'little') +
        json.dumps({'filename': filename, 'num_chunks': num_chunks}).encode('utf-8'))
    print(qr_data[0])
    qr_image = qrcode.make(qr_data)
    qr_images.append(qr_image)
    for i in range(num_chunks):
        chunk = data[i * max_size:(i + 1) * max_size]
        qr_data = base64.b64encode((i + 1).to_bytes(1, 'little') + chunk)
        print(qr_data[:10])
        qr_image = qrcode.make(qr_data)
        qr_images.append(qr_image)

    return qr_images


def get_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    return data


if __name__ == "__main__":
    data = get_file(sys.argv[1])
    imgs = generate_qr_from_file(data, filename=sys.argv[1].split('/')[-1])

    print(len(imgs))
    for i, img in enumerate(imgs):
        path = os.path.join('./imgs', f'{i}.png')
        img.save(path)

    images = []
    for filename in Path('imgs').iterdir():
        images.append(imageio.imread(filename))
    imageio.mimwrite('res.gif', images)
# print(qr_images)
# for qr_image in qr_images:
#     qr_image
# image.show()
