import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1
POWER_PIN = 21


# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout


def spi_readout():
    SPICLK = 18
    SPIMISO = 23
    SPIMOSI = 24
    SPICS = 25

    # set up the SPI interface pins
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)

    # 10k trim pot connected to adc #0
    potentiometer_adc = 0

    # read the analog pin
    return readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)


def power_on():
    GPIO.setup(POWER_PIN, GPIO.OUT)
    GPIO.output(POWER_PIN, True)


def power_off():
    GPIO.output(POWER_PIN, False)


if __name__ == "__main__":
    power_on()
    time.sleep(1)
    print("Hygrometer value %d" % spi_readout())
    time.sleep(1)
    power_off()
    GPIO.cleanup()
