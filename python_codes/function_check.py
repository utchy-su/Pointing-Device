import matplotlib.pyplot as plt
import numpy as np

MAX = 40

def linear(x):
    if -MAX <= x <= MAX:
        return x/MAX
    return np.sign(x) * 1.0

def tanh(x):
    if -MAX <= x <= MAX:
        return np.sign(x)*np.sqrt(abs(x)/MAX)
    return np.sign(x) * 1.0

def x_square(x):
    if -MAX <= x <= MAX:
        return np.sign(x) * (x/MAX)**2
    return np.sign(x) * 1.0

theta = np.arange(-50, 50 , 0.01)

lin_y, tan_y, xx_y = [], [], []

for t in theta:
    lin_y.append(linear(t))
    tan_y.append(tanh(t))
    xx_y.append(x_square(t))

plt.plot(theta, lin_y, label="$\dot{X}=k_x\\theta$", linewidth=4, alpha=0.7)
plt.plot(theta, tan_y, label="$\dot{X}=k_x\sqrt{\\theta}$", color="orange", linewidth=4, alpha=0.7)
plt.plot(theta, xx_y, label="$\dot{X}=k_x\\theta^2$", color="green", linewidth=4, alpha=0.7)

plt.axhline(0, ls="--")
plt.axvline(0, ls="--")
plt.xlabel("tilt angle of head[deg]")
plt.ylabel("pointer velocity[px/s]")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
