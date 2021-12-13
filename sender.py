import math
import os

import qrcode


def generate_qr_from_file(file_path, max_size=100):
    with open(file_path, 'rb') as f:
        data = f.read()
    data = data * 5

    num_chunks = math.ceil(len(data) / max_size)
    qr_images = []

    for i in range(num_chunks):
        chunk = data[i * max_size:(i + 1) * max_size]
        qr_image = qrcode.make(chunk)
        qr_images.append(qr_image)

    return qr_images


if __name__ == "__main__":
    imgs = generate_qr_from_file('../test_files/sample.txt')
    for i, img in enumerate(imgs):
        path = os.path.join('../test_data', f'{i}.png')
        img.save(path)
# print(qr_images)
# for qr_image in qr_images:
#     qr_image
# image.show()
