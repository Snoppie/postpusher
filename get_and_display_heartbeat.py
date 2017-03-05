#!/usr/bin/env python2.7

import requests
import RPi.GPIO as GPIO
from threading import Thread
from multiprocessing import Pipe
import time
import json

def get_heartbeat(pipe):
    session = requests.Session()
    while True:
        data = session.get("http://ec2-54-93-71-88.eu-central-1.compute.amazonaws.com/heartbeat").text
        data = json.loads(data)["data"]
        if data["heartbeat"] == 0.0: data["heartbeat"] = 1
        pipe.send(data)
        time.sleep(1)

pipe_parent, pipe_child = Pipe()
thread = Thread(target=get_heartbeat, args=(pipe_child,))
thread.start()

HEART_GPIO=22
heartbeat_timeout=1.0
LED_ROT = 2
LED_GRUEN = 3
LED_BLAU = 4

try:
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(HEART_GPIO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_ROT, GPIO.OUT, initial= GPIO.LOW)
    GPIO.setup(LED_GRUEN, GPIO.OUT, initial= GPIO.LOW)
    GPIO.setup(LED_BLAU, GPIO.OUT, initial= GPIO.LOW)

    while True:
        GPIO.output(HEART_GPIO, GPIO.HIGH)
        time.sleep(.2)
        GPIO.output(HEART_GPIO, GPIO.LOW)
        time.sleep(.1)
        GPIO.output(HEART_GPIO, GPIO.HIGH)
        time.sleep(.2)
        GPIO.output(HEART_GPIO, GPIO.LOW)
        heartbeat_sleep=max(heartbeat_timeout - .5, .1)
        time.sleep(heartbeat_sleep)
        if (pipe_parent.poll()):
            data = pipe_parent.recv()
            heartbeat_timeout=60.0/float(data["heartbeat"])

            if data["face"]:
                GPIO.output(LED_ROT,GPIO.LOW)
                GPIO.output(LED_GRUEN,GPIO.HIGH)
                GPIO.output(LED_BLAU,GPIO.LOW)
            else:
                GPIO.output(LED_ROT,GPIO.LOW)
                GPIO.output(LED_GRUEN,GPIO.LOW)
                GPIO.output(LED_BLAU,GPIO.HIGH)

            

# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
    GPIO.cleanup()

