import time
from threading import Thread
from util.constants import SERVO_DEFAULT_ANGLE

# determines if the automation is running or not.
running = False

# this is a dictionary that stores
# the last distances scanned by the servo
# the key is the angle and the value is the distance
last_distances = {}


def start_automation(car) -> None:
    """
    Handles the automation of the car.
    It will run until the running variable is set to False.

    :param car: the car instance
    :return: None
    """
    print("Starting automation")

    while running:
        # ensures that the last_distances dictionary is not empty
        # meanwhile, the car will be waiting for the distances.
        while len(last_distances) == 0:
            print("(⚠) No distances, waiting the servo to scan...")
            time.sleep(1)

        # if there is nothing in front of the car
        # then move forward
        if last_distances[SERVO_DEFAULT_ANGLE] > 20:
            print("Moving forward...")

            # FIXME: check if the engines ignore the start
            #   command if they are already running.

            # start engine if it's not already started
            car.start_engine()

            # then move forward
            car.move_forward()

            # FIXME: if move_forward does not need to be
            #   called again, then remove this sleep.
            #   and clear the last_distances dictionary
            #   to avoid the car to move forward again.

            # wait some time to check if there is something
            # in front of the car
            time.sleep(1)
            continue

        # copy the last distances
        distances = last_distances.copy()

        # delete the 0 angle since it is the front
        del distances[0]

        # now find the farthest angle
        farthest_angle = max(last_distances, key=last_distances.get)

        # FIXME: code below may not work, need testing to check how to move
        #   the car to the left or right

        # now stop the engine to turn the car to the farthest angle
        car.stop_engine()

        # if it is a negative angle, then turn left
        # otherwise turn right
        if farthest_angle < 0:
            print("Turning left")
            car.move_left()
        else:
            print("Turning right")
            car.move_right()

        # force the servo to scan again since the car direction
        # has changed, so the distances may have changed and the
        # front angle is not the same because the car turned.
        last_distances.clear()


def start_scan_loop(servo) -> None:
    """
    Creates a loop that will scan the environment
    and store the distances in the last_distances dictionary.
    It will run until the running variable is set to False.

    :param servo: the servo instance
    :return: None
    """
    while running:
        global last_distances
        last_distances = servo.scan()
        print("(✓) Scan complete, distances: ", last_distances)


def start(car, servo) -> None:
    """
    Starts the automation in another thread.

    :param car: the car instance
    :param servo: the servo instance
    :return: None
    """
    global running
    if running:
        print("(⚠) Automation is already running")
        return

    running = True

    # creates a thread that will scan the environment
    # and store the distances in the last_distances dictionary
    scan_thread = Thread(target=start_scan_loop, args=(servo,))
    scan_thread.start()

    # creates a thread that will handle the automation
    automation_thread = Thread(target=start_automation, args=(car,))
    automation_thread.start()


def stop() -> None:
    """
    Stops the automation.

    :return: None
    """
    global running
    running = False
