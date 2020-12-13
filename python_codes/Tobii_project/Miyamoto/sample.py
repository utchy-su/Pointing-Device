import numpy as np
import pandas as pd
import scipy.stats as st
from statsmodels.stats.multicomp import pairwise_tukeyhsd

damping = pd.read_excel("./Damping.xlsx")
stiffness = pd.read_excel("./Stiffness.xlsx")

param = input("param?: ")

if param == "damping":
    data = damping
else:
    data = stiffness

N = len(data.normal)
data = np.hstack((data.normal, data.tandem, data.narrow, data.wide))
group = ["normal"]*N + ["tandem"]*N + ["narrow"]*N + ["wide"]*N

result = pairwise_tukeyhsd(data, group)
print(result)