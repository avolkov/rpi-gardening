#!/usr/bin/env python

from RPi import GPIO
import time

read_pin = 11
power_pin = 7

wait_settle = 0.3


def needs_watering():
    """
    Check if the orchid needs watering
    Return True if water is needed, False otherwise
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(power_pin, GPIO.OUT)
    GPIO.setup(read_pin, GPIO.IN)

    GPIO.output(power_pin, True)
    time.sleep(wait_settle)
    state = GPIO.input(read_pin)
    GPIO.output(power_pin, False)
    GPIO.cleanup()
    return bool(state)


if __name__ == "__main__":
    if needs_watering():
        print("Please water me")
    else:
        print("I'm fine")
