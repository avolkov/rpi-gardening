# MCP 3008 chip

## Adafruit article

https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/connecting-the-cobbler-to-a-mcp3008


The Raspberry Pi computer does not have a way to read analog inputs. It's a digital-only computer.

# To talk to MCP3008 Configure SPI interface

Install necessary dependencies


    # aptitude install python3-dev python3-rpi.gpio



# MCP Pinout

![MCP Pinout](mcp3008pin.gif)

Raspberry Pi Side --

**VDD** -- Power

**VREF** -- Analog voltage reference (used to change voltage scale)

**AGND** -- Analog Ground (used in precision circuitry), Connects to GND.

**CLK** -- Clock Pin

**DOUT** -- Data out from MCP3008

**DIN** -- Data in from Raspberry Pi

**CN** -- Chip select

# Wiring Diagram

|MCP 3008| Raspberry Pi| Cable Color|
|--------|-------------|------------|
|VDD     | 3.3V        | Red        |
|VREF    | 3.3V        | Red        |
|AGND    | GND         | Black      |
|CLK     | #18         | Orange     |
|DOUT    | #23         | Yellow     |
|DIN     | #24         | Blue       |
|CS      | #25         | Violet     |
|DGND    | GND         | Black      |


# Soil Hygrometer HL-01/YL-69

http://www.modmypi.com/electronics/sensors/soil-moisture-sensor

https://www.tiagoespinha.net/2014/05/project-how-to-easily-monitor-your-plants-soil-humidity/

The two pins from controller (HL-01) to the probe (YL-69) can be connected in any order.

Controller Pins

|HL-01|Breadbord|
|-----|---------|
|A0   | CH0     |
|D0   | Not used in analog mode |
|GND  | GND  |
|VCC  | 5V |

# Enable  SPI

Run `raspi-config`

Advanced Options -> SPI

Would you like the SPI interface to be enabled? `Yes`

Would you like the SPI kernel module to be loaded by  default? `Yes`

Reboot the pi.

# The code

Adopted from -- https://gist.github.com/ladyada/3151375


[mcp3008.py](mcp3008.py)


# Hygrometer readings

Potentiometer readings:

|Connection Type | Reading |
|----------------|---------|
|Air             | 1023    |
|Water           | 520-580 |
|Shorted Pins    | 40      |
|Soil watered 1 day ago| 520-560|


Screw adjuster trigger point for digital reading does not affect the sensitivity of analog readings. However, once inserted the readings gradually decreased from initial 560 to 517 a few minutes later.

# Controlling 5V rail with PN2222A Transistor


![pn2222a.png](pn222a.png)

**Collector** -- Input Voltage

**Base** -- Control current

**Emitter** -- Output Voltage


See [source/0002_hygrometer_power_control.py](source/0002_hygrometer_power_control.py) for controlling power to the device and only reading the values during power-on cycle

```python
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
```