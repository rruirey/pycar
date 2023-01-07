import time

import FakeRPi.GPIO as GPIO

from util.constants import *
from util.utiliities import angle_to_percent

# the angles to scan.
# limits are -90 and 90 since the servo motor
# can only move 180 degrees
angles = [
    -90, -45,  # left
    0,  # front
    45, 90  # right
]


def setup() -> None:
    """
    Sets up the servo motor.
    :return: None
    """

    # stops the servo motor
    GPIO.setup(SERVO, GPIO.OUT)

    # creates the PWM instance
    global pwm
    pwm = GPIO.PWM(SERVO, SERVO_FREQUENCY)

    # starts the servo motor at the default angle
    pwm.start(angle_to_percent(SERVO_DEFAULT_ANGLE))


def scan() -> dict[int, float]:
    """
    Scans the environment at the predefined angles.
    :return: a dictionary with the angle as key and the distance as value
    """
    distances = {}
    for angle in angles:
        distances[angle] = scan_angle(angle)
    return distances


def scan_angle(angle: int) -> float:
    """
    Scans the environment at the given angle.

    :param angle: the angle to scan
    :return: the distance in cm
    """

    # moves the servo to the given angle
    pwm.ChangeDutyCycle(angle_to_percent(angle))

    # gives the servo some time to move
    time.sleep(1)

    # start trigger
    GPIO.output(TRIGGER, True)

    # wait for the trigger to finish
    time.sleep(0.00001)

    # stop trigger and check for the distance
    return stop_trigger_and_check()


def stop_trigger_and_check() -> float:
    """
    Stops the trigger and checks the echo pin
    to get the distance.

    :return: the distance in cm
    """

    # stop trigger
    GPIO.output(TRIGGER, False)

    start = time.time()
    end = time.time() + 0.1

    # TODO: uncomment this
    # while GPIO.input(ECHO) == 0:
    #     start = time.time()
    # while GPIO.input(ECHO) == 1:
    #     end = time.time()

    elapsed = end - start
    return (elapsed * 34300) / 2
