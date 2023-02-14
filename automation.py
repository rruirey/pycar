import time
from threading import Thread
import servo
import car
from util.constants import SERVO_DEFAULT_ANGLE

# determines if the automation is running or not.
running = False

# this is a dictionary that stores
# the last distances scanned by the servo
# the key is the angle and the value is the distance
last_distances = {}


def start_automation() -> None:
    """
    Handles the automation of the car.
    It will run until the running variable is set to False.

    :return: None
    """
    print("Starting automation")
    while running:
        print("Scanning front angle...")

        # checks if there is something in front of the car
        distance = servo.scan_angle(SERVO_DEFAULT_ANGLE)

        print("Distance: " + str(distance))

        # if there is nothing in front of the car
        # then move forward
        if distance > 20:
            print("Moving forward...")
            car.start_engine()
            car.move_forward()
            continue

        print("Fixing car direction...")
        car.stop_engine()

        distances = servo.scan()
        farthest_angle = max(distances, key=distances.get)

        print("Farthest angle: " + str(farthest_angle) + " with distance: " + str(distances[farthest_angle]))

        # TODO: code below not finished since the car is not working
        #   and there is no way to test how to move the car to the right
        #   or left to fix the direction.

        if farthest_angle < SERVO_DEFAULT_ANGLE:
            # move right logic
            car.move_right()
            print("Moving right...")
        else:
            # move left logic
            car.move_left()
            print("Moving left...")


def start() -> None:
    """
    Starts the automation.

    :return: None
    """
    global running
    running = True

    # starts the automation in a new thread
    Thread(target=start_automation).start()
