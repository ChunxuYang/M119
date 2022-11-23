import serial
import time
import pygame


def start_reading(addr, pygameInstance, index=0):
    ser = serial.Serial(addr, 9600)
    while True:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        if line == "up":
            if index == 0:
                pygameInstance.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
            else:
                pygameInstance.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w))
        elif line == "down":
            # if pygame is initialized, move paddle down
            if index == 0:
                pygameInstance.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
            else:
                pygameInstance.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s))
        time.sleep(0.01)


def run_central(pygameInstance):
    start_reading("/dev/ttyACM0", pygameInstance, 0)
    start_reading("/dev/ttyACM1", pygameInstance, 1)
