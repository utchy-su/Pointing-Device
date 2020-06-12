import pygame
from pygame.locals import *
import math
import sys
import pandas as pd
import pprint
import pyautogui as pag

"""
ベースの円を描画するクラス
TODO: arduinoからの角度データの受取り(pyserialの実装)
"""
class Base:
    TGT_RADIUS = 15  # ターゲットの円の半径
    TGT_DIAMETER = 30 # ターゲットの円の直径
    LAYOUT_RADIUS = 200  # ターゲットを配置する大きい円周の半径
    LAYOUT_DIAMETER = 400  # ターゲットを配置する大きい演習の直径

    def __init__(self, screen, screen_size):
        if not isinstance(screen_size, tuple):
            raise TypeError("screen_size should be tuple")

        self.screen = screen  # スクリーンのサイズ(例：(500, 500))
        self.center = (int(screen_size[0]/2), int(screen_size[1]/2))  #スクリーンの中心座標
        self.__draw()

    def __del__(self):
        # デストラクタ。何もしないので無視していい。
        pass

    def update(self):
        pass
        #一度だけ描画すれば良いのでupdateは必要ない

    def __draw(self):
        #layout circle
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, Base.LAYOUT_RADIUS, 2)
        font = pygame.font.Font(None, 30)

        for i in range(16):
            x = int(450 + Base.LAYOUT_RADIUS * math.cos(math.pi * (i/8)))
            y = int(450 + Base.LAYOUT_RADIUS * math.sin(math.pi * (i/8)))

            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), Base.TGT_RADIUS)
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y), Base.TGT_RADIUS, 2)
            text = font.render(str(TaskAxis.ORDERS[i]), True, (0, 0, 0))
            self.screen.blit(text, (x, y))


class TaskAxis:
    TGT_RADIUS = Base.TGT_RADIUS - 3
    TGT_DIAMETER = Base.TGT_DIAMETER - 6
    LAYOUT_RADIUS = Base.LAYOUT_RADIUS
    LAYOUT_DIAMETER = Base.LAYOUT_DIAMETER

    ORDERS = [0, 8, 1, 9, 2, 10, 3, 11, 4, 12, 5, 13, 6, 14, 7, 15, 8]

    def __init__(self, count, screen):
        if count == len(TaskAxis.ORDERS):
            raise IndexError("index should be within orderes")
        self.count = count
        self.screen = screen
        self.__draw()

    def __del__(self):
        x_from = int(450 + 200 * math.cos(math.pi * (TaskAxis.ORDERS[self.count] / 8)))
        y_from = int(450 + 200 * math.sin(math.pi * (TaskAxis.ORDERS[self.count] / 8)))

        x_to = int(450 + 200 * math.cos(math.pi * (TaskAxis.ORDERS[self.count+1] / 8)))
        y_to = int(450 + 200 * math.sin(math.pi * (TaskAxis.ORDERS[self.count+1] / 8)))

        pygame.draw.circle(self.screen, (255, 255, 255), (x_from, y_from), TaskAxis.TGT_RADIUS)
        pygame.draw.circle(self.screen, (255, 255, 255), (x_to, y_to), TaskAxis.TGT_RADIUS)
        pygame.draw.line(self.screen, (255, 255, 255), (x_from, y_from), (x_to, y_to), 5)
        pygame.draw.circle(self.screen, (0, 0, 0), (x_from, y_from), Base.TGT_RADIUS, 2)
        pygame.draw.circle(self.screen, (0, 0, 0), (x_to, y_to), Base.TGT_RADIUS, 2)


    """
    Draw a task axis. Constructor executes this method.
    """
    def __draw(self):
        x_from = int(450 + 200 * math.cos(math.pi * (TaskAxis.ORDERS[self.count] / 8)))
        y_from = int(450 + 200 * math.sin(math.pi * (TaskAxis.ORDERS[self.count] / 8)))

        x_to = int(450 + 200 * math.cos(math.pi * (TaskAxis.ORDERS[self.count+1] / 8)))
        y_to = int(450 + 200 * math.sin(math.pi * (TaskAxis.ORDERS[self.count+1] / 8)))

        pygame.draw.circle(self.screen, (255, 0, 0), (x_from, y_from), TaskAxis.TGT_RADIUS)
        pygame.draw.circle(self.screen, (255, 0, 0), (x_to, y_to), TaskAxis.TGT_RADIUS)
        pygame.draw.line(self.screen, (20, 128, 20), (x_from, y_from), (x_to, y_to), 5)

"""
描画と軌跡の記録用
"""
class Tester:

    TGT_RADIUS = 15
    TGT_DIAMETER = 30
    ALLOWABLE_ERROR = 100

    def __init__(self, path):
        self.x = {}
        self.y = {}
        self.time = {}

        self.path = path

    def __isInCircle(self, counter, x, y) -> bool:
        x_to = int(450 + 200 * math.cos(math.pi * (TaskAxis.ORDERS[counter + 1] / 8)))
        y_to = int(450 + 200 * math.sin(math.pi * (TaskAxis.ORDERS[counter + 1] / 8)))

        distance = int(math.sqrt((x-x_to)**2 + (y-y_to)**2))

        return distance <= Tester.TGT_RADIUS

    def __saveToExcel(self):
        #TODO: 各回ごとにtime, x, yの順で格納していく

        new_data_frame = {}

        for i in range(15):
            new_data_frame['x from ' + str(i) + ' to ' + str(i+1)] = self.x[i]
            new_data_frame['y from ' + str(i) + ' to ' + str(i+1)] = self.y[i]
            new_data_frame['time from ' + str(i) + ' to ' + str(i+1)] = self.time[i]

        print(new_data_frame.keys())

        df = pd.DataFrame.from_dict(new_data_frame, orient='index').T

        print(df)

        df.to_excel(self.path)

    def __testMouseMove(self, counter):
        x_from = int(450 + 200 * math.cos(math.pi * (TaskAxis.ORDERS[counter] / 8)))
        y_from = int(450 + 200 * math.sin(math.pi * (TaskAxis.ORDERS[counter] / 8)))

        # task axis に沿ってマウスカーソルを動かす
        x_to = int(450 + 200 * math.cos(math.pi * (TaskAxis.ORDERS[counter + 1] / 8)))
        y_to = int(450 + 200 * math.sin(math.pi * (TaskAxis.ORDERS[counter + 1] / 8)))

        x_mid = int((x_from + x_to) / 2)
        y_mid = int((y_from + y_to) / 2)

        if i == 1:
            pygame.mouse.set_pos(x_from, y_from)
            pygame.time.wait(100)
        elif i == 2:
            pygame.mouse.set_pos(x_mid, y_mid)
            pygame.time.wait(100)
        elif i == 3:
            pygame.mouse.set_pos(x_mid, y_mid)
            pygame.time.wait(100)
        elif i == 4:
            pygame.mouse.set_pos(x_to, y_to)
            pygame.time.wait(100)
        else:
            x, y = pag.position()
            pag.leftClick(x, y)


    def __isDriftingAway(self, x, y, counter):
        x_from = int(450 + 200 * math.cos(math.pi * (TaskAxis.ORDERS[counter] / 8)))
        y_from = int(450 + 200 * math.sin(math.pi * (TaskAxis.ORDERS[counter] / 8)))

        # task axis に沿ってマウスカーソルを動かす
        x_to = int(450 + 200 * math.cos(math.pi * (TaskAxis.ORDERS[counter + 1] / 8)))
        y_to = int(450 + 200 * math.sin(math.pi * (TaskAxis.ORDERS[counter + 1] / 8)))

        a = -(y_to - y_from)
        b = (x_to - x_from)
        c = -x_to * y_from + y_to * x_from

        dist = abs(a*x + b*y + c)/math.sqrt(a**2 + b**2)

        return dist > Tester.ALLOWABLE_ERROR


    def main(self):
        screen_size = (900, 900)
        pygame.init()
        screen = pygame.display.set_mode(screen_size)
        screen.fill((255, 255, 255))
        pygame.display.set_caption(u"new tester without serial com")


        base = Base(screen, screen_size)
        counter = 0 # click counter
        test = None

        time_record = []
        x_record = []
        y_record = []

        # wait until the user clicks anywhere in the window
        isClicked = False
        test = TaskAxis(counter, screen)

        while not isClicked:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    isClicked = self.__isInCircle(-1, x, y)
                    #最初の円をクリックすればカウントが始まる


        #描画を続けるループ。右上のXボタンを押せば強制終了出来る
        while True:
            pygame.display.update()
            now = pygame.time.get_ticks()
            x, y = pygame.mouse.get_pos()

            # abort the task if the cursor is drifting away too much
            if self.__isDriftingAway(x, y, counter):
                time_record = []
                x_record = []
                y_record = []
                x_from = int(450 + 200 * math.cos(math.pi * (TaskAxis.ORDERS[counter] / 8)))
                y_from = int(450 + 200 * math.sin(math.pi * (TaskAxis.ORDERS[counter] / 8)))
                pygame.mouse.set_pos(x_from, y_from)


            time_record.append(now)
            x_record.append(x)
            y_record.append(y)

            # self.__testMouseMove(counter)
            # if i == 5:
            #     i = 1
            # else:
            #     i += 1

            for event in pygame.event.get():
                if event.type == QUIT:
                    del test
                    pygame.display.update()
                    pygame.time.wait(3000)
                    sys.exit()

                if event.type == KEYDOWN:
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    if counter == 14:
                        self.time[counter] = time_record
                        self.x[counter] = x_record
                        self.y[counter] = y_record
                        counter += 1
                        del test
                        self.__saveToExcel()
                        return

                    if self.__isInCircle(counter, x, y):
                        self.time[counter] = time_record
                        self.x[counter] = x_record
                        self.y[counter] = y_record
                        time_record = []
                        x_record = []
                        y_record = []
                        counter += 1
                        del test
                        test = TaskAxis(counter, screen)


if __name__ == "__main__":
    path = "./test.xlsx"
    # 例：デスクトップにtest.xlsxという名前で保存したいのであれば
    #    C:Users/FUJITSU/Desktop/test.xlsx  というパスになるかと思います。
    test = Tester(path)
    test.main()
