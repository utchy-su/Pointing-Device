import serial
import time


class Serial:
    """
    シリアル通信で角度を取得するクラス

    Attributes
    ----------
    ser : pySerial obj
    """

    def __init__(self, com="/dev/ttyACM0", baud=9600):
        self.ser = None
        try:
            self.ser = serial.Serial(com, baud, timeout=None)

        except:
            while self.ser is None:
                self.ser = serial.Serial(com, baud, timeout=None)
                time.sleep(0.5)

    def read(self):
        line = self.ser.readline()
        line = line.decode().split(";")

        try:
            roll = line[0]
            pitch = line[1]
        except IndexError as e:
            roll = None
            pitch = None

        return roll, pitch