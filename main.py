import car
import servo
import automation

import interface.interface as interface


def main():
    # set up the servo motor
    servo.setup()

    # set up and start the car
    car.reset()
    car.setup()
    car.start_engine()

    # starts the automation
    automation.start(car, servo)

    # creates the window the last because
    # it will block the execution since it
    # runs in the main thread.
    interface.start()


if __name__ == '__main__':
    main()
