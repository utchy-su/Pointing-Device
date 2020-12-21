import pygame
from pygame.locals import *
import numpy as np


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

    def __init__(self, count, screen, orders, tgt_radius, layout_radius, allowable_err, center):
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
        orders : list
            クリックする円の順番を格納するリストです
        allowable_err : int
            なぞり経路からのズレの許容範囲です。
            この範囲を示すように緑の帯を描画します。これを超えるとカーソルがもとのターゲットに戻されます。
        center : tuple
            Layout circleの中心座標
        """
        self.count = count
        self.screen = screen
        self.__tgt_radius = tgt_radius
        self.__layout_radius = layout_radius
        self.__orders = orders
        self.__allowable_err = allowable_err
        self.center_x = center[0]
        self.center_y = center[1]
        self.font = pygame.font.Font(None, 50)
        self.__draw()
        self.__showCount()

    def __del__(self):
        """
        デストラクタです。TaskAxisオブジェクトが消えるときにdraw()関数で描画していた線の上に
        白線を描画することで元々あった線を消しています。
        """
        x_from = int(self.center_x + 200 * np.cos(np.pi * (self.__orders[self.count] / 8)))
        y_from = int(self.center_y + 200 * np.sin(np.pi * (self.__orders[self.count] / 8)))

        x_to = int(self.center_x + 200 * np.cos(np.pi * (self.__orders[self.count+1] / 8)))
        y_to = int(self.center_y + 200 * np.sin(np.pi * (self.__orders[self.count+1] / 8)))

        pygame.draw.circle(self.screen, (255, 255, 255), (x_from, y_from), self.__tgt_radius-3)
        pygame.draw.circle(self.screen, (255, 255, 255), (x_to, y_to), self.__tgt_radius-3)
        pygame.draw.line(self.screen, (255, 255, 255), (x_from, y_from), (x_to, y_to), 5)
        pygame.draw.circle(self.screen, (0, 0, 0), (x_from, y_from), self.__tgt_radius, 2)
        pygame.draw.circle(self.screen, (0, 0, 0), (x_to, y_to), self.__tgt_radius, 2)

    def __draw(self):
        """
        self.countの値に応じて該当する二円を結ぶように線を描画します。
        """
        x_from = int(self.center_x + 200 * np.cos(np.pi * (self.__orders[self.count] / 8)))
        y_from = int(self.center_y + 200 * np.sin(np.pi * (self.__orders[self.count] / 8)))

        x_to = int(self.center_x + 200 * np.cos(np.pi * (self.__orders[self.count+1] / 8)))
        y_to = int(self.center_y + 200 * np.sin(np.pi * (self.__orders[self.count+1] / 8)))

        pygame.draw.line(self.screen, (20, 128, 20), (x_from, y_from), (x_to, y_to), self.__allowable_err*2)
        pygame.draw.line(self.screen, (255, 255, 255), (x_from, y_from), (x_to, y_to), 5)
        pygame.draw.circle(self.screen, (255, 0, 0), (x_from, y_from), self.__tgt_radius)
        pygame.draw.circle(self.screen, (255, 0, 0), (x_to, y_to), self.__tgt_radius)

    def __showCount(self):
        text = self.font.render("click attempt: " + str(self.count+1), True, (0, 0, 0))
        self.screen.blit(text, [20, 20])

