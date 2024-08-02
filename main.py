from threading import Thread
import keyboard1 as kb
from queue import Queue
import time

q = Queue()


def constrain(val, min_val, max_val):
    if val < min_val: return min_val
    if val > max_val: return max_val
    return val


def pid(input, setpoint, kp, ki, kd, dt, minOut, maxOut):
    err = setpoint - input
    integral = 0
    prevErr = 0
    integral = constrain(integral + err * dt * ki, minOut, maxOut)
    d = (err - prevErr) / dt
    prevErr = err
    return constrain(err * kp + integral + d * kd, minOut, maxOut)


def tracker1():
    while True:
        track = q.get()

        if track > 0:
            kb.key_press(kb.SC_RIGHT)
        if track < 0:
            kb.key_press(kb.SC_LEFT)


th = Thread(target=tracker1, daemon=True)

