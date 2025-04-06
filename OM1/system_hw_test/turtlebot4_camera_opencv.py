import time

import cv2
import numpy as np
import zenoh
import os


def listener(sample):
    bytesI = sample.payload.to_bytes()
    print(f"Received {len(sample.payload)}")
    X = np.frombuffer(bytesI, dtype=np.uint8)
    # for some reason the first 76 numbers are trash?
    # some sort of metadata header?
    Xc = X[76:187576]
    rgb = np.reshape(Xc, (250, 250, 3))
    cv2.imwrite("front_image.jpg", rgb)


if __name__ == "__main__":

    with zenoh.open(zenoh.Config()) as session:
        urid = os.getenv("URID") 
        camera = session.declare_subscriber(f"{urid}/pi/oakd/rgb/preview/image_raw", listener)
        print("Zenoh is open")
        while True:
            print("Waiting for camera messages")
            time.sleep(1)
