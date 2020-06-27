"""New_tester.pyの機能に関して

    * Author: S.Uchino
    * Base, TasxAxisの2クラスは完全に無視で構いません。(内容の理解は必要ない)
    * Testerクラスの使い方さえわかればとりあえずは運用できます。

Todo:
"""

import pygame
from pygame.locals import *
import math
import sys
import pandas as pd
import pprint
import pyautogui as pag

class Base:
    """Baseクラスの機能

    ベースの大きい円周を描画とターゲットの小さい円を描画するクラスです。
    コンストラクタでscreenオブジェクトとスクリーンサイズ(width, height)を受け取ります。

    Attributes
    ----------
    tgt_radius : int
        ターゲット円の半径
    tgt_diameter : int
        ターゲット円の直径
    layout_radius : int
        レイアウトの円周の半径
    layout_diameter : int
        レイアウトの円周の直径
    screen : 'pygame object'
        screenオブジェクト
    center : tuple
        スクリーンの中心座標(e.g. (100, 100))
    """

    def __init__(self, screen, screen_size, tgt_radius, layout_radius):
        """
        コンストラクタです.

        Parameters
        ----------
        screen : pygame object
            pygameのAPIでreturnされるオブジェクトです。
        screen_size : tuple
            スクリーンのサイズをタプルで指定してください。例：(900, 900)
        """
        if not isinstance(screen_size, tuple):
            raise TypeError("screen_size should be tuple")

        self.screen = screen  # スクリーンのサイズ(例：(500, 500))
        self.center = (int(screen_size[0]/2), int(screen_size[1]/2))  #スクリーンの中心座標
        self.__tgt_radius = tgt_radius
        self.__layout_radius = layout_radius
        self.__draw()

    def __draw(self):
        """
        この関数で大きい円周を一つ、小さいターゲット円を16個描画します。
        """
        #大きい方の円の描画です。
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, self.__layout_radius, 2)
        font = pygame.font.Font(None, 30)

        #小さい方の円を16回描画します。
        for i in range(16):
            x = int(450 + self.__layout_radius * math.cos(math.pi * (i/8)))
            y = int(450 + self.__layout_radius * math.sin(math.pi * (i/8)))

            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), self.__tgt_radius)
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y), self.__tgt_radius, 2)


class TaskAxis:
    """
    Testerクラスから何回目のクリックかのカウントを受け取り、そのカウントに応じてtask axisを描画します。

    Attributes
    ----------
    tgt_radius : int
        ターゲット円の半径。
    layout_radius : int
        レイアウト円の半径。
    orders : list
        右端の円から半時計回りに0, 1, 2, 3,...と番号振ってます。n回目のクリックでORDERS[n]が赤く塗られます。
    count : int
        今何回目のクリックかを示します
    screen : pygame object
        pygameのAPIで作成したscreenオブジェクトです
    """

    def __init__(self, count, screen, orders, tgt_radius, layout_radius):
        """
        コンストラクタです。self.countの値に応じて__draw()関数を呼び出し、該当する二円を結ぶように線を描画します。

        Parameters
        ----------
        count : int
            今何回目のクリックかをTesterクラスから受け取ります。
        screen : pygame object
            screenオブジェクトです
        tgt_radius : int
            ターゲット円の半径です。デフォルトは15
        layout_radius : int
            レイアウト円の半径です。デフォルトは200
        """
        self.count = count
        self.screen = screen
        self.__tgt_radius = tgt_radius
        self.__layout_radius = layout_radius
        self.__orders = orders
        self.__draw()

    def __del__(self):
        """
        デストラクタです。TaskAxisオブジェクトが消えるときにdraw()関数で描画していた線の上に
        白線を描画することで元々あった線を消しています。
        """
        x_from = int(450 + 200 * math.cos(math.pi * (self.__orders[self.count] / 8)))
        y_from = int(450 + 200 * math.sin(math.pi * (self.__orders[self.count] / 8)))

        x_to = int(450 + 200 * math.cos(math.pi * (self.__orders[self.count+1] / 8)))
        y_to = int(450 + 200 * math.sin(math.pi * (self.__orders[self.count+1] / 8)))

        pygame.draw.circle(self.screen, (255, 255, 255), (x_from, y_from), self.__tgt_radius-3)
        pygame.draw.circle(self.screen, (255, 255, 255), (x_to, y_to), self.__tgt_radius-3)
        pygame.draw.line(self.screen, (255, 255, 255), (x_from, y_from), (x_to, y_to), 5)
        pygame.draw.circle(self.screen, (0, 0, 0), (x_from, y_from), self.__tgt_radius, 2)
        pygame.draw.circle(self.screen, (0, 0, 0), (x_to, y_to), self.__tgt_radius, 2)

    def __draw(self):
        """
        self.countの値に応じて該当する二円を結ぶように線を描画します。
        """
        x_from = int(450 + 200 * math.cos(math.pi * (self.__orders[self.count] / 8)))
        y_from = int(450 + 200 * math.sin(math.pi * (self.__orders[self.count] / 8)))

        x_to = int(450 + 200 * math.cos(math.pi * (self.__orders[self.count+1] / 8)))
        y_to = int(450 + 200 * math.sin(math.pi * (self.__orders[self.count+1] / 8)))

        pygame.draw.circle(self.screen, (255, 0, 0), (x_from, y_from), self.__tgt_radius)
        pygame.draw.circle(self.screen, (255, 0, 0), (x_to, y_to), self.__tgt_radius)
        pygame.draw.line(self.screen, (20, 128, 20), (x_from, y_from), (x_to, y_to), 5)


class Tester:
    """
    このクラス内でwhileループを回してデータを取得します。
    カーソルのx,y座標とプログラム開始からの経過時間を一定周期で取得し続けます。

    Attributes
    ----------
    TGT_RADIUS : int
        ターゲット円の半径です
    LAYOUT_RADIUS : int
        レイアウト円の半径です
    ALLOWABLE_ERROR : int
        内野が私用で使ってます。無視してください。
    ORDERS : list
        クリックする円の順番をリストとして保存しています。
    x : dict
        {1: [100, 111], 2:[2, 100, ..]}というように、n回目のクリックをするまでに
        カーソルが辿った軌跡のx座標を記録します
    y : dict
        x座標に同じ。
    time : dict
        経過時間をxと同じように記録します。
    path : str
        記録用のexcelファイルの保存場所です。
    """

    __TGT_RADIUS = 15
    __LAYOUT_RADIUS = 200
    __ALLOWABLE_ERROR = 100
    __ORDERS = [0, 8, 1, 9, 2, 10, 3, 11, 4, 12, 5, 13, 6, 14, 7, 15, 8]

    def __init__(self, path, screen_size=(900, 900)):
        """
        x, y, 経過時間を保持するdictを空にして初期化します。
        excelファイル保存用のパスをstrで取得します

        Parameters
        ----------
        path : str
            excelファイル保存用のパスのstr
        screen_size : tuple
            実験用ウインドウのサイズを指定してください。デフォルトでは(900, 900)
        """
        self.x = {}
        self.y = {}
        self.time = {}
        self.__base = None
        self.__test = None
        self.__screen_size = screen_size
        self.path = path

    @staticmethod
    def get_tgt_radius():
        """
        ターゲット円の半径のgetter
        """
        return Tester.__TGT_RADIUS

    @staticmethod
    def get_layout_radius():
        """
        レイアウト円の半径のgetter
        """
        return Tester.__LAYOUT_RADIUS

    @staticmethod
    def get_allowable_error():
        """
        許容できるMEの値のGetter
        """
        return Tester.__ALLOWABLE_ERROR

    @staticmethod
    def get_orders():
        """
        クリックする円の順番のgetter
        """
        return Tester.__ORDERS

    @staticmethod
    def set_tgt_radius(rad):
        """
        ターゲット円の半径のsetter
        """
        Tester.__TGT_RADIUS = rad

    @staticmethod
    def set_layout_radius(rad):
        """
        レイアウト円の半径のsetter
        """
        Tester.__LAYOUT_RADIUS = rad

    @staticmethod
    def set_orders(new_orders):
        """
        クリックする円の順番のsetter
        """
        if len(Tester.__ORDERS) != len(new_orders):
            raise Exception("すべての円を一度はクリックするように順番を設定してください")
        Tester.__ORDERS = new_orders

    def __get_from_and_to(self, counter):
        """
        出発地->目的地のx,y座標を求めます

        Parameters
        ----------
        counter : int
            今何回目のクリックかを示す

        Returns:
            x_from : int
            y_from : int
            x_to : int
            y_to : int
        """

        orders = Tester.__ORDERS
        x_from = int(450 + 200 * math.cos(math.pi * (orders[counter] / 8)))
        y_from = int(450 + 200 * math.sin(math.pi * (orders[counter] / 8)))

        # task axis に沿ってマウスカーソルを動かす
        x_to = int(450 + 200 * math.cos(math.pi * (orders[counter + 1] / 8)))
        y_to = int(450 + 200 * math.sin(math.pi * (orders[counter + 1] / 8)))

        return x_from, y_from, x_to, y_to

    def __isInCircle(self, counter, x, y) -> bool:
        """
        カーソルの座標(x, y)が与えられたとき、そのカーソルがクリックするべきターゲット内に
        入っているかを判別します。

        Parameters
        ----------
        counter : int
            今何回目のクリックかを示します。
        x : int
            カーソルのx座標です。
        y : int
            カーソルのy座標です。

        Return
        ------
            カーソルが円内ならTrue. False otherwise.
        """
        _, _, x_to, y_to = self.__get_from_and_to(counter)

        distance = int(math.sqrt((x-x_to)**2 + (y-y_to)**2))

        return distance <= Tester.get_tgt_radius()

    def __saveToExcel(self):
        """
        インスタンス変数(dict)として保持したx, y, timeをpandasのデータフレームに変換して
        excelファイルに保存する関数です。dfが表になります。

        Notes:
            excelに保存したくないときはこの関数をコメントアウトしてください。
        """
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
        """
        ユニットテスト用の関数。無視でいいです。
        """
        x_from, y_from, x_to, y_to = self.__get_from_and_to(counter)
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
        """
        内野が私用で使ってます。無視でいいです。
        """
        x_from, y_from, x_to, y_to = self.__get_from_and_to(counter)

        a = -(y_to - y_from)
        b = (x_to - x_from)
        c = -x_to * y_from + y_to * x_from

        dist = abs(a*x + b*y + c)/math.sqrt(a**2 + b**2)

        return dist > Tester.__ALLOWABLE_ERROR


    def main(self):
        """
        エントリーポイントです。
        """
        pygame.init()
        screen = pygame.display.set_mode(self.__screen_size)
        screen.fill((255, 255, 255))  # スクリーンの色を白に
        pygame.display.set_caption(u"new tester without serial com")


        # ベースになるレイアウト円とターゲット円を描画します。
        self.__base = Base(screen, self.__screen_size, Tester.__TGT_RADIUS, Tester.__LAYOUT_RADIUS)
        counter = 0 # click counter
        test = None

        # i-1回目->i回目のクリックの間のカーソルの動きを一時的に保存します。
        time_record = []
        x_record = []
        y_record = []

        # プログラムを開始します。最初のなぞり経路を描画します。
        isClicked = False
        self.__test = TaskAxis(counter, screen, Tester.__ORDERS, Tester.__TGT_RADIUS, Tester.__LAYOUT_RADIUS)

        # isClickedがFalse、すなわち最初の円をクリックしていない限りプログラムが
        # 進行しないようにしてあります。
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
            now = pygame.time.get_ticks() #現時点での経過時間を取得
            x, y = pygame.mouse.get_pos() #現時点でのカーソル座標を取得

            # ここから358行目まで内野が私用で使ってるコードなので無視でいいです
            """
            if self.__isDriftingAway(x, y, counter):
                time_record = []
                x_record = []
                y_record = []
                x_from = int(450 + 200 * math.cos(math.pi * (TaskAxis.ORDERS[counter] / 8)))
                y_from = int(450 + 200 * math.sin(math.pi * (TaskAxis.ORDERS[counter] / 8)))
                pygame.mouse.set_pos(x_from, y_from)
            """

            time_record.append(now) #経過時間を記録
            x_record.append(x) #カーソル座標を記録
            y_record.append(y) #カーソル座標を記録

            # self.__testMouseMove(counter)
            # if i == 5:
            #     i = 1
            # else:
            #     i += 1

            for event in pygame.event.get():
                # もしウインドウ右上のxボタンが押されたらプログラムを終了
                if event.type == QUIT:
                    del self.__test
                    pygame.display.update()
                    pygame.time.wait(3000)
                    sys.exit()

                #　何かキーを押すとプログラムを終了
                if event.type == KEYDOWN:
                    sys.exit()

                # もしマウスのボタンを押すと
                if event.type == MOUSEBUTTONDOWN:
                    # counter==14のときプログラムを終了
                    if counter == 14:
                        self.time[counter] = time_record
                        self.x[counter] = x_record
                        self.y[counter] = y_record
                        counter += 1
                        del self.__test
                        self.__saveToExcel()
                        return

                    # もしクリックした座標がターゲットの円内なら...
                    if self.__isInCircle(counter, x, y):
                        self.time[counter] = time_record
                        self.x[counter] = x_record
                        self.y[counter] = y_record
                        time_record = []
                        x_record = []
                        y_record = []
                        counter += 1
                        del self.__test # counter回目に対応するTaskAxisを消す
                        self.__test = TaskAxis(counter, screen, Tester.__ORDERS, Tester.__TGT_RADIUS, Tester.__LAYOUT_RADIUS)


if __name__ == "__main__":
    path = "./test.xlsx"
    # 例：デスクトップにtest.xlsxという名前で保存したいのであれば
    #    C:Users/FUJITSU/Desktop/test.xlsx  というパスになるかと思います。
    test = Tester(path)
    test.main()
