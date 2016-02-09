import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

POWER_PIN = 21
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25


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


def spi_setup():
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    GPIO.setup(POWER_PIN, GPIO.OUT)


def spi_readout(adc_pin):
    # read the analog pin
    return readadc(adc_pin, SPICLK, SPIMOSI, SPIMISO, SPICS)


def power_on():

    GPIO.output(POWER_PIN, True)


def power_off():
    GPIO.output(POWER_PIN, False)


def adc_to_temp(readout):
    millivolts = readout * (3300.0 / 1024.0)
    temp_c = ((millivolts - 100.0) / 10.0) - 40.0
    print("Readout ", readout)
    print("Millivolts ", millivolts)
    print("Temp C", temp_c)
    return temp_c

if __name__ == "__main__":
    HYGROMETER = 0
    TEMP = 1
    spi_setup()
    power_on()
    time.sleep(1)
    temp = adc_to_temp(spi_readout(TEMP))
    print("Hygrometer value %d" % spi_readout(HYGROMETER))
    print("Temp sensor: %.1f C" % temp)
    time.sleep(1)
    power_off()
    GPIO.cleanup()
