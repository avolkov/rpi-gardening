from RPi import GPIO
import time
power_pin = 7

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(power_pin, GPIO.OUT)

    GPIO.output(power_pin, True)
    time.sleep(10)
    GPIO.cleanup()
