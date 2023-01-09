import time

import RPi.GPIO as GPIO

from util.constants import *

start_engines = [
    START_ENGINE_1,
    START_ENGINE_2
]

engines = [
    ENGINE_1A, ENGINE_1B,
    ENGINE_2A, ENGINE_2B
]


def reset() -> None:
    GPIO.cleanup()


def setup() -> None:
    print("setting up")

    GPIO.setmode(GPIO.BCM)

    # sets engines to OUT
    for engine in engines:
        GPIO.setup(engine, GPIO.OUT)

    for engine in start_engines:
        GPIO.setup(engine, GPIO.OUT)

    # configure sensors
    setup_ultra()

    print("finished setting up")


def setup_ultra():
    GPIO.setup(TRIGGER, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIGGER, False)


def start_engine() -> None:
    for engine in start_engines:
        GPIO.output(engine, GPIO.HIGH)


def stop_engine() -> None:
    # stops start engines
    for engine in start_engines:
        GPIO.output(engine, GPIO.LOW)

    # stops engines
    for engine in engines:
        GPIO.output(engine, GPIO.LOW)


def move_forward() -> None:
    GPIO.output(ENGINE_1A, GPIO.HIGH)
    GPIO.output(ENGINE_1B, GPIO.LOW)
    GPIO.output(ENGINE_2A, GPIO.HIGH)
    GPIO.output(ENGINE_2B, GPIO.LOW)


def move_backwards() -> None:
    GPIO.output(ENGINE_1A, GPIO.LOW)
    GPIO.output(ENGINE_1B, GPIO.HIGH)
    GPIO.output(ENGINE_2A, GPIO.LOW)
    GPIO.output(ENGINE_2B, GPIO.HIGH)


def move_right() -> None:
    GPIO.output(ENGINE_1A, GPIO.HIGH)
    GPIO.output(ENGINE_1B, GPIO.LOW)
    GPIO.output(ENGINE_2A, GPIO.LOW)
    GPIO.output(ENGINE_2B, GPIO.HIGH)


def move_left() -> None:
    GPIO.output(ENGINE_1A, GPIO.LOW)
    GPIO.output(ENGINE_1B, GPIO.HIGH)
    GPIO.output(ENGINE_2A, GPIO.HIGH)
    GPIO.output(ENGINE_2B, GPIO.LOW)
