"""
    Program to read data from PLANTOWER PMS5003

    Modified from program to read data from NovaFitness SDS011 by
    Nils Jacob Berland
    njberland@gmail.com / njberland@sensar.io
    +47 40800410
    
    Modified by
    Szymon Jakubiak

    Measured values of PM1, PM2.5 and PM10 are in ug/m^3
    Number of particles in #/cm^3
"""
import serial
from time import sleep

# Specify serial port address
ser_port = "COM38"
ser = serial.Serial(ser_port, baudrate=9600, stopbits=1, parity="N",  timeout=2)

try:
    while True:
        ser.flushInput()
        s = ser.read(32)
        # Check if data header is correct
        if s[0] == int("42",16) and s[1] == int("4d",16):
            cs = (s[30] * 256 + s[31])   # check sum
            # Calculate check sum value
            check = 0
            for i in range(30):
                check += s[i]
            # Check if check sum is correct
            if check == cs:
                # PM1, PM2.5 and PM10 values in ug/m^3
                pm1_hb_atm = s[10]
                pm1_lb_atm = s[11]
                pm1_atm = float(pm1_hb_atm * 256 + pm1_lb_atm)
                pm25_hb_atm = s[12]
                pm25_lb_atm = s[13]
                pm25_atm = float(pm25_hb_atm * 256 + pm25_lb_atm)
                pm10_hb_atm = s[14]
                pm10_lb_atm = s[15]
                pm10_atm = float(pm10_hb_atm * 256 + pm10_lb_atm)

                # Number of particles bigger than 0.3 um, 0.5 um, etc. in #/cm^3
                part_03_hb = s[16]
                part_03_lb = s[17]
                part_03 = int(part_03_hb * 256 + part_03_lb)
                part_05_hb = s[18]
                part_05_lb = s[19]
                part_05 = int(part_05_hb * 256 + part_05_lb)
                part_1_hb = s[20]
                part_1_lb = s[21]
                part_1 = int(part_1_hb * 256 + part_1_lb)
                part_25_hb = s[22]
                part_25_lb = s[23]
                part_25 = int(part_25_hb * 256 + part_25_lb)
                part_5_hb = s[24]
                part_5_lb = s[25]
                part_5 = int(part_5_hb * 256 + part_5_lb)
                part_10_hb = s[26]
                part_10_lb = s[27]
                part_10 = int(part_10_hb * 256 + part_10_lb)
                
                print("PM1:", pm1_atm, "ug/m^3  PM2.5:", pm25_atm, "ug/m^3  PM10:", pm10_atm, "ug/m^3")
                print(">0.3:", part_03, " >0.5:", part_05, " >1.0:", part_1, " >2.5:", part_25, " >5:", part_5, " >10:", part_10)
except KeyboardInterrupt:
    ser.close()
    print("Serial port closed")
