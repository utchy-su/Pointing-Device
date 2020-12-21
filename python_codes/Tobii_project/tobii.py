from collections import deque
import tobii_research as tb
import numpy as np
# import win32api


class Tobii:
    """
    Tobii Fusionから視線データをsubscribeします．
    キャリブレーションは別途付属ソフトで行う方が速いし楽です．
    """

    def __init__(self, screen_size):
        """
        Tobiiのセットアップをします．
        eye_trackerオブジェクトに現在接続しているTobiiの情報が渡される
        """
        self.width = 1920
        self.height = 1080
        self.eye_tracker = tb.find_all_eyetrackers()[0]
        self.x = None
        self.y = None
        self.screen_size = screen_size
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]

    def get_coordinates(self):
        if (self.x is None) or (self.y is None):
            return 0, 0

        return int(self.x), int(self.y)

    def gaze_data_callback(self, gaze_data):
        # 左目の視線と画面平面の交点座標(x, y)
        xl, yl = gaze_data.left_eye.gaze_point.position_on_display_area

        # 右目の視線と画面平面の交点座標(x, y)
        xr, yr = gaze_data.right_eye.gaze_point.position_on_display_area

        # subscribeに失敗しているときはnanが返ってくるので，何もせずreturn
        if np.isnan(xl) or np.isnan(xr) or np.isnan(yl) or np.isnan(yr):
            return

        # 左目と右目の視線の平均をリストに格納
        self.x = (self.screen_width * (xl+xr))//2
        self.y = (self.screen_height * (yl+yr))//2

    def start_subscribing(self):
        self.eye_tracker.subscribe_to(tb.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=False)

    def end_subscribing(self):
        self.eye_tracker.unsubscribe_from(tb.EYETRACKER_GAZE_DATA, self.gaze_data_callback)
