import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from Data_store import DataFrames


class VectorValidation:

    def __init__(self, path):
        self.path = path
        self.data = DataFrames(path, flattening_range=1)

    def draw(self, count):
        LX, LY = 1920, 1080
        gridwidth = 10
        X, Y = np.meshgrid(np.arange(0, LX, gridwidth), np.arange(0, LY, gridwidth))

        sr = 5
        px = self.data.get_cods()['x'][count][::sr]
        py = self.data.get_cods()['y'][count][::sr]
        gx = self.data.get_gaze_cods()['x'][count][::sr]
        gy = self.data.get_gaze_cods()['y'][count][::sr]
        t = self.data.get_timestamp()[count][::sr]
        print(t)

        N = len(px)
        vx = [(px[i+1] - px[i])/(t[i+1] - t[i]) for i in range(N-1)] + [0]
        vy = [(py[i+1] - py[i])/(t[i+1] - t[i]) for i in range(N-1)] + [0]
        dx = [(gx[i] - px[i]) for i in range(N)]
        dy = [(gy[i] - py[i]) for i in range(N)]

        plt.plot(px, py, "-o")
        plt.plot(gx, gy, "x")
        plt.quiver(px, py, vx, vy, color="green", label="pointer velocity vector", angles="xy", scale_units="xy", width=0.005, scale=0.05, minshaft=5)
        plt.quiver(px, py, dx, dy, color="red", label="gaze-pointer vector", angles="xy", scale_units="xy", width=0.005, scale=3, minshaft=5)
        plt.grid()
        plt.legend()
        # plt.xlim(0, LX)
        # plt.ylim(0, LY)
        plt.draw()
        plt.show()

    def tlead_validation(self, count):
        smpran = 5 # sampling range
        px = self.data.get_cods()['x'][count]
        py = self.data.get_cods()['y'][count]
        gx = self.data.get_gaze_cods()['x'][count]
        gy = self.data.get_gaze_cods()['y'][count]
        t = self.data.get_timestamp()[count]

        px = px[::smpran]
        py = py[::smpran]
        gx = gx[::smpran]
        gy = gy[::smpran]
        t = t[::smpran]

        N = len(px)
        vx = [(px[i + 1] - px[i]) / (t[i + 1] - t[i]) for i in range(N - 1)]
        vy = [(py[i + 1] - py[i]) / (t[i + 1] - t[i]) for i in range(N - 1)]
        dx = [(gx[i] - px[i]) for i in range(N - 1)]
        dy = [(gy[i] - py[i]) for i in range(N - 1)]

        tlead = []
        for vx_, vy_, dx_, dy_ in zip(vx, vy, dx, dy):
            num = vx_*dx_ + vy_*dy_
            den = vx_*vx_ + vy_*vy_
            if num == 0.0 or den == 0.0:
                tlead.append(tlead[-1])
            else:
                tlead.append(num/den)
            print(vx_, vy_, dx_, dy_, num, den)
        print(tlead)
        tlead = [1 if t<0 else 0 for t in tlead]
        print(tlead)

if __name__ == "__main__":
    path = ".\\data\\Uchino\\mouse\\test1.xlsx"
    test = VectorValidation(path)
    test.draw(5)
    test.tlead_validation(5)
