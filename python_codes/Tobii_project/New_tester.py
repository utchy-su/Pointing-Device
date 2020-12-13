"""New_tester.pyの機能に関して

    * Author: S.Uchino
    * Base, TasxAxisの2クラスは完全に無視で構いません。(内容の理解は必要ない)
    * Testerクラスの使い方さえわかればとりあえずは運用できます。
    * Tobiiのdocs-> http://developer.tobiipro.com/python/python-sdk-reference-guide.html

TODO:
    * ターゲット軸の色は要検討
    * コマンド引数使わない版を作る
"""

import pygame
from pygame.locals import *
import math
import time
import pandas as pd
import pyautogui as pag
from win32api import GetSystemMetrics
import os

from serial_com import Serial
from tobii import Tobii
from base import Base
from task_axis import TaskAxis


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
    DWELLING_TIME : int
        ターゲット内にDWELLING_TIME(ms)静止するとクリック扱いになります。
        単位がミリ秒であることに注意してください。
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

    __TGT_RADIUS = 30
    __LAYOUT_RADIUS = 200
    __ALLOWABLE_ERROR = 30
    __ORDERS = [0, 8, 1, 9, 2, 10, 3, 11, 4, 12, 5, 13, 6, 14, 7, 15, 8]
    __DWELLING_TIME = 1000 #ms

    def __init__(self, path, screen_size=(1920, 1080), measure_angles=True, com_port="/dev/ttyACM0"):
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
        self.__identify_os()
        self.x = {}  # coordinate about x-axis
        self.y = {}  # coordinate about y-axis
        self.time = {}  # time passed of each time
        self.roll = {}  # roll angle of each time
        self.pitch = {}  # pitch angle of each time
        self.gaze_x = {}
        self.gaze_y = {}
        self.isSuccessful = []
        self.__base = None
        self.__test = None
        self.__screen_size = (GetSystemMetrics(0), GetSystemMetrics(1))
        self.__center_x, self.__center_y = screen_size[0]//2, screen_size[1]//2
        self.path = path
        if measure_angles:
            self.ser = Serial(com=com_port)
        self.__measure_angles = measure_angles  # bool
        self.__tobii = Tobii(screen_size)
        self.__tobii.start_subscribing()

    def __identify_os(self):
        if os.name == "nt":
            return
        else:
            exit("Try windows OS. Quitting...")

    @staticmethod
    def getTgtRadius():
        """
        ターゲット円の半径のgetter
        """
        return Tester.__TGT_RADIUS

    @staticmethod
    def getLayoutRadius():
        """
        レイアウト円の半径のgetter
        """
        return Tester.__LAYOUT_RADIUS

    @staticmethod
    def getAllowableError():
        """
        許容できるMEの値のGetter
        """
        return Tester.__ALLOWABLE_ERROR

    @staticmethod
    def getOrders():
        """
        クリックする円の順番のgetter
        """
        return Tester.__ORDERS

    @staticmethod
    def setTgtRadius(rad):
        """
        ターゲット円の半径のsetter
        """
        Tester.__TGT_RADIUS = rad

    @staticmethod
    def setLayoutRadius(rad):
        """
        レイアウト円の半径のsetter
        """
        Tester.__LAYOUT_RADIUS = rad

    @staticmethod
    def setOrders(new_orders):
        """
        クリックする円の順番のsetter
        """
        if len(Tester.__ORDERS) != len(new_orders):
            raise Exception("すべての円を一度はクリックするように順番を設定してください")
        Tester.__ORDERS = new_orders

    @staticmethod
    def getDwellingTime():
        """
        クリック判別の閾値時間のgetter
        """
        return Tester.__DWELLING_TIME

    @staticmethod
    def setDwellingtime(new_time):
        """
        クリック判別の閾値時間のsetter
        """
        Tester.__DWELLING_TIME = new_time

    def __getFromAndTo(self, counter):
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
        x_from = int(self.__center_x + 200 * math.cos(math.pi * (orders[counter] / 8)))
        y_from = int(self.__center_y + 200 * math.sin(math.pi * (orders[counter] / 8)))

        # task axis に沿ってマウスカーソルを動かす
        x_to = int(self.__center_x + 200 * math.cos(math.pi * (orders[counter + 1] / 8)))
        y_to = int(self.__center_y + 200 * math.sin(math.pi * (orders[counter + 1] / 8)))

        return x_from, y_from, x_to, y_to

    def __isInCircle(self, counter, x, y) -> bool:
        """
        カーソルの座標(x, y)が与えられたとき、そのカーソルがクリックするべきターゲット内に
        入っているかを判別します。

        :param counter: 今何回目のクリックかを示す
        :type counter: int
        :param x: カーソルのx座標
        :type x: int
        :param y: カーソルのy座標
        :type y: int

        :return: カーソルが円内ならTrue. False otherwise.
        """
        _, _, x_to, y_to = self.__getFromAndTo(counter)

        distance = int(math.sqrt((x-x_to)**2 + (y-y_to)**2))

        return distance <= Tester.getTgtRadius()

    def __saveToExcel(self):
        """
        インスタンス変数(dict)として保持したx, y, timeをpandasのデータフレームに変換して
        excelファイルに保存する関数です。dfが表になります。

        excelに保存したくないときはこの関数をコメントアウトしてください。

        TODO: hoge
        """
        new_data_frame = {}

        for i in range(15):
            new_data_frame['x from ' + str(i) + ' to ' + str(i+1)] = self.x[i]
            new_data_frame['y from ' + str(i) + ' to ' + str(i+1)] = self.y[i]
            new_data_frame['gaze x from ' + str(i) + ' to ' + str(i+1)] = self.gaze_x[i]
            new_data_frame['gaze y from ' + str(i) + ' to ' + str(i+1)] = self.gaze_y[i]
            new_data_frame['time from ' + str(i) + ' to ' + str(i+1)] = self.time[i]
            new_data_frame['roll from ' + str(i) + ' to ' + str(i+1)] = self.roll[i]
            new_data_frame['pitch from ' + str(i) + ' to ' + str(i+1)] = self.pitch[i]
        new_data_frame["fail success ratio"] = self.isSuccessful

        print(new_data_frame.keys())

        df = pd.DataFrame.from_dict(new_data_frame, orient='index').T

        print(df)

        df.to_excel(self.path)

    def __testMouseMove(self, counter):
        """
        ユニットテスト用の関数。無視でいいです。

        Parameters
        ----------
        counter : int
            何回目のクリックか示す
        """
        x_from, y_from, x_to, y_to = self.__getFromAndTo(counter)
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
        x_from, y_from, x_to, y_to = self.__getFromAndTo(counter)

        a = -(y_to - y_from)
        b = (x_to - x_from)
        c = -x_to * y_from + y_to * x_from

        dist = abs(a*x + b*y + c)/math.sqrt(a**2 + b**2)

        return dist > Tester.__ALLOWABLE_ERROR

    def __addListToDict(self, counter, time, x, y, roll, pitch, gaze_x, gaze_y):
        self.time[counter] = time
        self.x[counter] = x
        self.y[counter] = y
        self.roll[counter] = roll
        self.pitch[counter] = pitch
        self.gaze_x[counter] = gaze_x
        self.gaze_y[counter] = gaze_y

    def main(self):
        """
        エントリーポイントです。
        """
        pygame.init()
        screen = pygame.display.set_mode(self.__screen_size, FULLSCREEN)
        screen.fill((255, 255, 255))  # スクリーンの色を白に
        pygame.display.set_caption(u"new tester without serial com")


        # ベースになるレイアウト円とターゲット円を描画します。
        self.__base = Base(screen, self.__screen_size, Tester.__TGT_RADIUS, Tester.__LAYOUT_RADIUS)
        counter = 0 # click counter
        trajectory_counter = 0
        test = None

        # i-1回目->i回目のクリックの間のカーソルの動きを一時的に保存します。
        time_record = []
        x_record = []
        y_record = []
        roll_record = []
        pitch_record = []
        gaze_x_record = []
        gaze_y_record = []
        isSuccessful = True

        # record the first time when the cursor entered into the target
        first_entry = None # not None when the cursor entered. None otherwise

        # プログラムを開始します。最初のなぞり経路を描画します。
        isClicked = False
        c = (self.__center_x, self.__center_y)
        self.__test = TaskAxis(counter, screen, Tester.__ORDERS, Tester.__TGT_RADIUS, Tester.__LAYOUT_RADIUS, Tester.__ALLOWABLE_ERROR, c)

        # isClickedがFalse、すなわち最初の円をクリックしていない限りプログラムが
        # 進行しないようにしてあります。
        while not isClicked:
            pygame.display.update()
            now = pygame.time.get_ticks()
            x, y = pygame.mouse.get_pos()
            if self.__isInCircle(-1, x, y):
                if first_entry is not None:
                    dwelling_time = now - first_entry
                    if dwelling_time >= Tester.__DWELLING_TIME:
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
                else:
                    first_entry = pygame.time.get_ticks()
            else:
                first_entry = None
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    isClicked = self.__isInCircle(-1, x, y)
                    # 最初の円をクリックすればカウントが始まる

        # 描画を続けるループ。右上のXボタンを押せば強制終了出来る
        while True:
            pygame.display.update()
            now = pygame.time.get_ticks()  # 現時点での経過時間を取得
            x, y = pygame.mouse.get_pos()  # 現時点でのカーソル座標を取得
            if self.__measure_angles:
                roll, pitch = self.ser.read()
            else:
                roll, pitch = 0, 0

            # reset the position if the cursor drifts away too much
            if self.__isDriftingAway(x, y, counter):
                isSuccessful = False
                # x_from = int(450 + 200 * math.cos(math.pi * (Tester.__ORDERS[counter] / 8)))
                # y_from = int(450 + 200 * math.sin(math.pi * (Tester.__ORDERS[counter] / 8)))
                #pygame.mouse.set_pos(x_from, y_from)

            # append the trajectory to the record
            time_record.append(now)  # 経過時間を記録
            x_record.append(x)  # カーソル座標を記録
            y_record.append(y)  # カーソル座標を記録
            roll_record.append(roll)
            pitch_record.append(pitch)

            # draw the trajectory of the cursor
            pygame.draw.circle(screen, (0, 0, 0), (x, y), 2, 0)

            # Tobiiで得た視線データを描画する
            gaze_x, gaze_y = self.__tobii.get_coordinates()
            # self.__tobii.move_to_gaze_position()
            gaze_x_record.append(gaze_x)
            gaze_y_record.append(gaze_y)
            # print(gaze_x, gaze_y)
            # pygame.draw.circle(screen, color=(122, 0, 122), center=(gaze_x, gaze_y), radius=3)

            # カーソルが一定時間以上ターゲット円内で静止しないとクリックとしてみなされない
            if self.__isInCircle(counter, x, y):
                if first_entry is not None:
                    # first_entryとnowを比較
                    dwelling_time = now - first_entry #millisec
                    if dwelling_time >= Tester.__DWELLING_TIME:
                        # dwelling_time以上ターゲット内に静止しているならば、
                        # eventにMOUSEBUTTONDOWNを追加することでクリック扱いになります
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
                else:
                    first_entry = pygame.time.get_ticks()
            else:
                first_entry = None  # set first_entry to None if the cursor is out of targets


            for event in pygame.event.get():
                # もしウインドウ右上のxボタンが押されたらプログラムを終了
                if event.type == QUIT:
                    del self.__test
                    pygame.display.update()
                    pygame.time.wait(3000)
                    sys.exit()

                #　何かキーを押すとプログラムを終了
                if event.type == KEYDOWN:
                    self.__tobii.end_subscribing()
                    sys.exit()

                # もしマウスのボタンを押すと
                if event.type == MOUSEBUTTONDOWN:
                    # counter==14のときプログラムを終了
                    if counter == 14:
                        self.__addListToDict(counter, time_record, x_record, y_record, roll_record, pitch_record, gaze_x_record, gaze_y_record)
                        self.isSuccessful.append(isSuccessful)
                        counter += 1
                        del self.__test
                        self.__saveToExcel()
                        self.__tobii.end_subscribing()
                        return

                    # もしクリックした座標がターゲットの円内なら...
                    if self.__isInCircle(counter, x, y):
                        self.__addListToDict(counter, time_record, x_record, y_record, roll_record, pitch_record, gaze_x_record, gaze_y_record)
                        self.isSuccessful.append(isSuccessful)
                        time_record = []
                        x_record = []
                        y_record = []
                        roll_record = []
                        pitch_record = []
                        gaze_x_record = []
                        gaze_y_record = []
                        isSuccessful = True
                        counter += 1
                        screen.fill((255, 255, 255))  # whiting out the screen
                        self.__base = Base(screen, self.__screen_size, Tester.__TGT_RADIUS, Tester.__LAYOUT_RADIUS) # draw the circles
                        del self.__test # counter回目に対応するTaskAxisを消す
                        self.__test = TaskAxis(counter, screen, Tester.__ORDERS, Tester.__TGT_RADIUS, Tester.__LAYOUT_RADIUS, Tester.__ALLOWABLE_ERROR, c)

if __name__ == "__main__":
    import glob
    import sys
    """
    path = sys.argv[1]
    measure_angles = sys.argv[2]

    file_list = glob.glob("./**", recursive=True)
    #ディレクトリ内のファイル名を全取得
    if path in file_list:
        exit("specified file name already exists!")
    # 重複するファイル名は作れない

    #もし第三引数 measure_angles = Trueならデバイスから角度のデータを取得して保存
    if measure_angles == "True":
        angles = True
    else:
        angles = False
    """

    path = ".\\data\\Murakami\\sqrt_10\\test20.xlsx"
    # ファイルを保存したい場所のパスに保存先のフォルダを指定
    # file_name.xlsxを保存するときのファイル名に変更

    file_list = glob.glob(".\\data\\**", recursive=True)
    if path in file_list:
        exit("同名ファイルが存在します．違うファイル名を指定してください．")

    # COMPORT = "/dev/ttyACM0"
    COMPORT = "COM13"  # ここは自分のarduinoのCOMポート番号に変更

    # 例：デスクトップにtest.xlsxという名前で保存したいのであれば
    #    C:Users/FUJITSU/Desktop/test.xlsx  というパスになるかと思います。
    test = Tester(path, measure_angles=True, com_port=COMPORT)
    test.main()
