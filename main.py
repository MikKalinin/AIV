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
        if 100 < track < 200:
            kb.key_press(kb.SC_RIGHT, 0.5)
        if -200 < track < -100:
            kb.key_press(kb.SC_LEFT, 0.5)
        if 200 < track < 300:
            kb.key_press(kb.SC_RIGHT, 0.7)
        if -300 < track < -200:
            kb.key_press(kb.SC_LEFT, 0.7)
        q.task_done()


th = Thread(target=tracker, daemon=True)

