"""
Note:
    1. I use the 6-axis IMU sensor (MPU-6050)
    2. If you use other types, then you need to check the data sheet.
"""

import serial
import math


class MySerial:

    def __init__(self, COM, BaudRate=19200):
        self.ser = serial.Serial(COM, BaudRate)
        # construct with COM number and BaudRate
        # use this class like ser = Serial(14, 9600)
        # COM number is

    def get_raw(self):
        """
        data sent from the microcomputer must be:
        [ax; ay; az; gx; gy; gz; t]

        :return:
        """

        try:
            data = self.ser.readline()
            data = data.decode().split(';')

        except:
            data = [0, 0, 0, 0, 0, 0, 0]
            print("Oops, something going wrong.\n")

        return data

    def get_angle(self):
        """
        input sent by the microcomputer must be like:
        [angX, angY]
        :return: pitch, roll
        """
        try:
            data = self.ser.readline()
            data = data.decode().split(';')
            acc_pitch = data[0]
            acc_roll = data[1]
            gain = data[2]

            return acc_pitch, acc_roll, gain

        except:
            data = ['err', 'err']
            print("Oops, something going wrong.\n")
            return 'err', 'err'

    def close(self):
        self.ser.close()
