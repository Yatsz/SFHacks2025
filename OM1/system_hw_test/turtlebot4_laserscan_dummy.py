import random
import time

import zenoh

random.seed()


def read_temp():
    return random.randint(15, 30)


if __name__ == "__main__":
    with zenoh.open(zenoh.Config()) as session:
        key = "pi/scan"
        pub = session.declare_publisher(key)
        while True:
            t = read_temp()
            buf = f"{t}"
            print(f"Putting Data ('{key}': '{buf}')...")
            pub.put(buf)
            time.sleep(1)
