import car
import servo
import automation

import interface.interface as interface


def main():
    # set up and start the car
    car.reset()
    car.setup()

    # set up the servo motor
    servo.setup()

    # starts the automation
    automation.start()

    # creates the window the last because
    # it will block the execution since it
    # runs in the main thread.
    interface.start()


if __name__ == '__main__':
    main()
