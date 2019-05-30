import pygame
from pygame.locals import *
import openpyxl as px
import numpy as np
import pandas as pd


class Window:

    def __init__(self, path):
        self.screen_size = (900, 900)
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption(u"trajectory check")
        self.diameter = 30

        # initialize and draw all circles
        pygame.draw.circle(self.screen, (0, 0, 0), (450, 450), 200, 2)
        for i in range(16):
            x = 450 + 200 * np.cos(np.pi * (i / 8))
            y = 450 + 200 * np.sin(np.pi * (i / 8))
            pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), self.diameter)
            pygame.draw.circle(self.screen, (0, 0, 0), (int(x), int(y)), self.diameter, 2)

        # load the excel data
        self.df = pd.read_excel(path)

        self.order = self.df['orders']

    def __draw_all(self):
        for i in range(16):
            x = 450 + 200 * np.cos(np.pi * (i / 8))
            y = 450 + 200 * np.sin(np.pi * (i / 8))
            pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), self.diameter)
            pygame.draw.circle(self.screen, (0, 0, 0), (int(x), int(y)), self.diameter, 2)

    def __coordinates2(self):
        columns = self.df.columns
        x_columns = columns.str.contains('x from')  # get coordinates from data sheet
        y_columns = columns.str.contains('y from')

        x = self.df.loc[:, x_columns]  # extract columns that contain coordinates data
        y = self.df.loc[:, y_columns]

        return x, y

    def __trajectory(self, x, y, click_count):
        x_index = 'x from ' + str(click_count) + ' to ' + str(click_count+1)
        y_index = 'y from ' + str(click_count) + ' to ' + str(click_count+1)
        x_interval = x[x_index].dropna(how='all').astype(int)
        y_interval = y[y_index].dropna(how='all').astype(int)

        for i in range(len(x_interval) - 1):
            pygame.draw.circle(self.screen, (0, 0, 255), (x_interval[i], y_interval[i]), 2)

    def __trajectory_remove(self, x, y, click_count):
        x_index = 'x from ' + str(click_count) + ' to ' + str(click_count + 1)
        y_index = 'y from ' + str(click_count) + ' to ' + str(click_count + 1)
        x_interval = x[x_index].dropna(how='all').astype(int)
        y_interval = y[y_index].dropna(how='all').astype(int)

        for i in range(len(x_interval) - 1):
            pygame.draw.circle(self.screen, (255, 255, 255), (x_interval[i], y_interval[i]), 2)

    def __tgt_circle(self, order_now):
        x = 450 + 200 * np.cos(np.pi * (order_now / 8))
        y = 450 + 200 * np.sin(np.pi * (order_now / 8))
        pygame.draw.circle(self.screen, (255, 0, 0), (int(x), int(y)), self.diameter)

    def __tgt_circle_remover(self, order_now):
        x = 450 + 200 * np.cos(np.pi * (order_now / 8))
        y = 450 + 200 * np.sin(np.pi * (order_now / 8))
        pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), self.diameter)
        pygame.draw.circle(self.screen, (0, 0, 0), (int(x), int(y)), self.diameter, 2)

    def __tgt_line(self, click_count, order_now, order):
        x = 450 + 200 * np.cos(np.pi * (order_now / 8))
        y = 450 + 200 * np.sin(np.pi * (order_now / 8))
        x_nxt = 450 + 200 * np.cos(np.pi * (order[click_count + 1]) / 8)
        y_nxt = 450 + 200 * np.sin(np.pi * (order[click_count + 1]) / 8)

        pygame.draw.line(self.screen, (20, 128, 20), (x, y), (x_nxt, y_nxt), 5)

    def __tgt_line_remover(self, click_count, order_now, order):
        x = 450 + 200 * np.cos(np.pi * (order_now / 8))
        y = 450 + 200 * np.sin(np.pi * (order_now / 8))
        x_prev = 450 + 200 * np.cos(np.pi * (order[click_count - 1]) / 8)
        y_prev = 450 + 200 * np.sin(np.pi * (order[click_count - 1]) / 8)

        pygame.draw.line(self.screen, (255, 255, 255), (x_prev, y_prev), (x, y), 5)

        pygame.draw.circle(self.screen, (0, 0, 0), (int(x_prev), int(y_prev)), self.diameter, 2)

    def __update(self, click_count, order_now, order, x, y):
        self.__tgt_circle_remover(order[click_count - 1])
        self.__tgt_line_remover(click_count, order[click_count], order)
        self.__trajectory_remove(x, y, click_count)
        self.__draw_all()
        self.__tgt_circle(order[click_count])
        self.__tgt_circle(order[click_count + 1])
        self.__tgt_line(click_count, order_now, order)
        self.__trajectory(x, y, click_count+1)

    def main(self):
        click_count = 0
        order = self.order  # excelファイルから引っ張ってきたやつ．leftmostのデータ
        x, y = self.__coordinates2()
        print(x, y)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()

                if event.type == MOUSEBUTTONDOWN:
                    click_count += 1
                    self.__update(click_count, order[click_count], order, x, y)
            pygame.display.update()


if __name__ == '__main__':
    path = 'C:/Users/socre/Desktop/linear vs non-linear result/Self/linear/attempt1.xlsx'
    test = Window(path)
    test.main()
