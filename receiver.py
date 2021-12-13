import json
from time import time

import cv2
from pyzbar.pyzbar import decode
import base64


def get_chunk_number(chunk):
    chunk = base64.b64decode(chunk)
    chunk_number = int(chunk[0]) - 48
    data = chunk[1:]

    return chunk_number, data


def read_first_qr(chunk_data: str):
    data_dict = json.loads(chunk_data)

    return data_dict['filename'], data_dict['num_chunks']


def read_qr(img, method=None):
    """
    find and decode QR code in a single image

    Args:
        img:
        method:

    Returns:

    """
    chunk = ''
    if method == 'cv2':
        qrCodeDetector = cv2.QRCodeDetector()
        chunk, _, _ = qrCodeDetector.detectAndDecode(img)
    elif method == 'pyzbar':
        res = decode(img)
        if len(res) > 0:
            chunk = res[0].data  # .decode('utf-8')
            print(chunk)
    else:
        raise ValueError(f'method: {method} is not supported.')

    return chunk


def main(fps):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise ValueError("Cannot open camera")

    chunks = []
    chunk_counter = 1

    total_data = None

    # data from first QR code
    filename = None
    num_chunks = None

    prev = 0
    while True:
        time_elapsed = time() - prev
        ret, frame = cap.read()
        if time_elapsed > 1. / fps:
            prev = time()

            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            chunk = read_qr(gray, 'pyzbar')

            if chunk != '':
                chunk_num, chunk_data = get_chunk_number(chunk)
                print(f'curr chunk {chunk_num}')

                # first QR, header
                if chunk_num == 0:
                    filename, num_chunks = read_first_qr(chunk_data)
                    print(f'Reading file: {filename}, with {num_chunks} chunks.')

                elif chunk_num == chunk_counter:
                    print(f'got chunk no. {chunk_num}')
                    print(f'{chunk_data[:10]}')
                    chunks.append(chunk_data)
                    chunk_counter += 1

                elif chunk_num > chunk_counter:
                    print(f'missed the last qr, you\'re still on the {chunk_counter} image.')

                if chunk_num == num_chunks:
                    print(f'finished taking {num_chunks} chunks.')
                    total_data = b''.join(chunks)
                    with open('res.zip', 'wb') as f:
                        f.write(total_data)
                    break

            cv2.imshow('frame', gray)

            if cv2.waitKey(1) == ord('q'):
                break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    return total_data, filename


if __name__ == '__main__':
    FPS = 10
    print(main(FPS))
