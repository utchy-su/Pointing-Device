import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class CompareRoute:

    def __init__(self, path):
        self.path = path
        self.df = pd.read_excel(self.path)

    def compare_route(self, param):
        horizontal = self.df.MD[self.df.click == 1]
        vertical = self.df.MD[self.df.click == ]