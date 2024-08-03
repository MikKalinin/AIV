from threading import Thread
import keyboard1 as kb
from queue import Queue

q = Queue()


def tracker():
    per = 1
    while (track := q.get()) is not None:

        limit1 = 100
        limit2 = 200
        limit3 = 50

        if per > 3:
            kb.key_press(kb.SC_DEL, interval=0.1)
            per = 3

        if per < 1:
            kb.key_press(kb.SC_INS, interval=0.1)
            per = 1

        if -1*limit2 < track < limit2:
            kb.key_up(kb.SC_LEFT)
            kb.key_up(kb.SC_RIGHT)
            kb.key_down(kb.SC_UP)
            if per != 3 and per < 4:
                kb.key_press(kb.SC_INS, interval=0.1)
                per += 1

        elif track > limit2:
            kb.key_down(kb.SC_RIGHT)
            kb.key_up(kb.SC_UP)
            if per != 1:
                kb.key_press(kb.SC_DEL, interval=0.1)
                per -= 1

        elif limit3 < track < limit1:
            kb.key_press(kb.SC_LEFT, interval=0.03)
            kb.key_press(kb.SC_RIGHT, interval=0.01)

        elif -1*limit1 < track < -1*limit3:
            kb.key_press(kb.SC_RIGHT, interval=0.03)
            kb.key_press(kb.SC_LEFT, interval=0.01)

        elif track < limit2:
            kb.key_down(kb.SC_LEFT)
            kb.key_up(kb.SC_UP)
            if per != 1:
                kb.key_press(kb.SC_DEL, interval=0.1)
                per -= 1


th = Thread(target=tracker, daemon=True)
