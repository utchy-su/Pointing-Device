import pygame
from pygame.locals import *
import openpyxl as px
import numpy as np
import itertools
from pprint import pprint


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

        # loading the excel data
        self.wb = px.load_workbook(path)
        self.ws = self.wb.active

        self.order = [int(self.ws['A' + str(i + 2)].value) for i in range(14)]

    def __draw_all(self):
        for i in range(16):
            x = 450 + 200 * np.cos(np.pi * (i / 8))
            y = 450 + 200 * np.sin(np.pi * (i / 8))
            pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), self.diameter)
            pygame.draw.circle(self.screen, (0, 0, 0), (int(x), int(y)), self.diameter, 2)

    def __coordinates(self):
        alph = [chr(i) for i in range(65, 65 + 26)] + ['A' + chr(i) for i in range(65, 65 + 26)]
        x = []
        y = []
        for i in range(14):
            x_interval = []
            y_interval = []

            for row in range(self.ws.max_row):
                alph_x = alph[(i + 1) * 3 - 2]
                cell_x = alph_x + str(row + 2)

                if self.ws[cell_x].value is not None:
                    x_interval.append(int(self.ws[cell_x].value))

            for row in range(self.ws.max_row):
                alph_y = alph[(i + 1) * 3 - 1]
                cell_y = alph_y + str(row + 2)

                if self.ws[cell_y].value is not None:
                    y_interval.append(int(self.ws[cell_y].value))

            for period in range(len(x_interval)-50):
                x.append(np.mean(x_interval[period:period+50]))
                y.append(np.mean(y_interval[period:period+50]))
        return x, y

        """
        for row in range(self.ws.max_row):
            alph_x = alph[click_count * 2 - 1]
            cell_x = alph_x + str(row+2)

            if self.ws[cell_x].value is not None:
                x.append(int(self.ws[cell_x].value))

        for row in range(self.ws.max_row):
            alph_y = alph[click_count * 2]
            cell_y = alph_y + str(row+2)

            if self.ws[cell_y].value is not None:
                y.append(int(self.ws[cell_y].value))

        for xi, yi in itertools.product(x, y):
            pygame.draw.circle(self.screen, (0, 0, 0), (xi, yi), 1)

        """

    def __trajectory(self, x, y, click_count):
        x_interval = x[click_count]
        y_interval = y[click_count]

        for i in range(len(x_interval) - 1):
            pygame.draw.circle(self.screen, (0, 0, 255), (x_interval[i], y_interval[i]), 2)

    def __trajectory_remove(self, x, y, click_count):
        x_interval = x[click_count]
        y_interval = y[click_count]

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
        x, y = self.__coordinates()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()

                if event.type == MOUSEBUTTONDOWN:
                    click_count += 1
                    self.__update(click_count, order[click_count], order, x, y)
            pygame.display.update()


if __name__ == '__main__':
    path = 'PATH'
    test = Window(path)
    test.main()
