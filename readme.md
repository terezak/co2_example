# MH-Z19C

# About the MH-Z19X CO2 sensor

The MH-Z19 sensor is manufactured by Winsen Lt., China and the measurement method used is based on the non-dispersive infrared (NDIR) principle to detect the existence of CO2 in the air.
Key features according to the manufacturer are:

    good sensitivity.
    non-oxygen dependent.
    long life.
    built-in temperature compensation.
    UART serial interface and Pulse Width Modulation (PWM) output.

A nondispersive infrared sensor (or NDIR sensor) is a relatively simple spectroscopic sensor often used as a gas detector. It is nondispersive in the sense of optical dispersion since the infrared energy is allowed to pass through the atmospheric sampling chamber without deformation.
Principle of operation:
The main components of an NDIR sensor are an infrared source (lamp), a sample chamber or light tube, a light filter and an infrared detector. The IR light is directed through the sample chamber towards the detector. In parallel there is another chamber with an enclosed reference gas, typically nitrogen. The gas in the sample chamber causes absorption of specific wavelengths according to the Beer–Lambert law, and the attenuation of these wavelengths is measured by the detector to determine the gas concentration. The detector has an optical filter in front of it that eliminates all light except the wavelength that the selected gas molecules can absorb.

# Technical Parameters and Structure

https://www.winsen-sensor.com/d/files/infrared-gas-sensor/mh-z19c-pins-type-co2-manual-ver1_0.pdf

![Raspberry Pi with mh-z19](assets/images/rpi_mhz19.jpg)
![GPIO Pins Overview](https://cdn.sparkfun.com/r/600-600/assets/learn_tutorials/1/5/9/5/GPIO.png)

![GPIO Pins Overview](https://www.circuits.dk/wp-content/uploads/2017/06/CO2-sensor-MH-Z19-pinout.jpg)

# Calibrations

## Zero Point Calibration

This module has two methods for zero point calibration: hand-operated method and self-calibration. All the zero
point is at 400ppm CO2.

# Hand-operated method:
Connect module’s HD pin to low level(0V), lasting for 7 seconds at least. Before calibrating the zero point, please
ensure that the sensor is stable for more than 20 minutes at 400ppm ambient environment.

# Self-calibration function:
The self-calibration function means that after the sensor runs continuously for a period of time, it can
intelligently determine the zero point according to the environmental concentration and calibrate itself. The
calibration cycle is automatic calibration every 24 hours since power-on operation. The zero point of automatic
calibration is 400ppm.
The self-calibration function is suitable for office environment and home environment. However, it is not suitable
for agricultural greenhouses, breeding farms, cold storage and other places. In such places, self-calibration
function should be turned off. After the shutdown, users are required to periodically perform zero-point
detection on the sensors, and if necessary, perform zero calibration or manual zero calibration.


# Installation

### python 3.x
sudo pip3 install mh_z19

### read CO2 Sensor value
pi@raspberrypi:~ $ sudo python3 -m mh_z19
pi@raspberrypi pinout