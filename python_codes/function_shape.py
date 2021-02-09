import matplotlib.pyplot as plt
import numpy as np

def linear(x):
    if x < -40:
        return -1.0
    elif (-40 <= x) and (x <= 40):
        return x/40
    else:
        return 1.0

k = 15
x = np.arange(-45, 45, 1)
y = [k*linear(pos) for pos in x]

plt.plot(x, y)
plt.plot(0, 0, "o", label="(deg, output)=(0,0)")
# plt.tight_layout()
plt.xlabel("angle[deg]")
plt.ylabel("velocity[px/s]")
plt.legend()
plt.grid()
plt.show()