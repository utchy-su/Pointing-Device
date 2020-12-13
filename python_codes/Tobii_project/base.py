import pygame
import numpy as np

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
        self.center = (screen_size[0]//2, screen_size[1]//2)  #スクリーンの中心座標
        self.__tgt_radius = tgt_radius
        self.__layout_radius = layout_radius
        self.__draw()

    def __draw(self):
        """
        この関数で大きい円周を一つ、小さいターゲット円を16個描画します。
        """
        # 大きい方の円の描画です。
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, self.__layout_radius, 2)
        font = pygame.font.Font(None, 30)

        # 小さい方の円を16回描画します。
        for i in range(16):
            x = int(self.center[0] + self.__layout_radius * np.cos(np.pi * (i/8)))
            y = int(self.center[1] + self.__layout_radius * np.sin(np.pi * (i/8)))

            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), self.__tgt_radius)
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y), self.__tgt_radius, 2)
