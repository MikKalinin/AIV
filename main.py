from threading import Thread
import keyboard1 as kb
from queue import Queue

q = Queue()


def tracker():
    while True:
        track = q.get()
        print(track)
        if 0 < track < 100:
            kb.key_press(kb.SC_RIGHT)
        if -100 < track < 0:
            kb.key_press(kb.SC_LEFT)



th = Thread(target=tracker, daemon=True)

