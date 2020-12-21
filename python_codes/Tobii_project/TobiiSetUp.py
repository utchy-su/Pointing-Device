import tobii_research as tb
import pygame
import time
from pygame.locals import *
from win32api import GetSystemMetrics
import win32api
import numpy as np


class TobiiSetUp:
    x = []
    y = []

    def __init__(self):
        res_x = 1920
        res_y = 1080
        # print(res_x, res_y)
        self.w = res_x
        self.h = res_y
        self.eye_tracker = tb.find_all_eyetrackers()[0]
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), FULLSCREEN)
        # self.__display_setting()
        # self.calibration_points = self.__get_calibration_points()

    def __display_setting(self):
        """
        SDKから手動でキャリブレーションする場合，ディスプレイとTobii本体との位置関係を設定する必要がある．

        :return:
        """
        # 学生室のディスプレイの下部にセットする場合
        bottom_left = (-297, 0, -5)
        bottom_right = (297, 0, -5)
        top_left = (-297, 370, 134)
        top_right = (297, 370, 134)
        height = 340
        width = 297*2

        new_display_area = dict()
        new_display_area['top_left'] = top_left
        new_display_area['top_right'] = top_right
        new_display_area['bottom_left'] = bottom_left
        new_display_area['bottom_right'] = bottom_right
        new_display_area['height'] = height
        new_display_area['width'] = width

        # self.eye_tracker.set_display_area(tb.DisplayArea(new_display_area))

    def calibrate(self):
        """
        画面上5点でキャリブレーションを行う．
        :return:
        """
        calibrator = tb.ScreenBasedCalibration(self.eye_tracker)
        calibrator.enter_calibration_mode()

        if tb.EYETRACKER_NOTIFICATION_CALIBRATION_MODE_ENTERED:
            print("calibration mode")
        else:
            print("oops, something occurred. terminating the program")

        is_data_collected = False
        for i in range(5):
            while not is_data_collected:
                print("Calibration at the point " + str(i+1))
                self.screen.fill((0, 0, 0))
                x, y = self.calibration_points[i]
                # pygame.draw.circle(self.screen, color=(255, 255, 255), center=(20, 20), radius=10)
                # pygame.draw.circle(self.screen, color=(255, 255, 255), center=(1900, 1080), radius=10)
                pygame.draw.circle(self.screen, color=(255, 255, 255), center=(x, y), radius=10)
                pygame.display.update()
                time.sleep(1.0)
                calibration_status = calibrator.collect_data(x, y)
                time.sleep(2.0)

                is_data_collected = calibration_status == "calibration_status_success"
            is_data_collected = False
            #TODO: 画面上の点を見るように指示をだす
        calibration_result = calibrator.compute_and_apply()
        if calibration_result is None:
            print("calibration failed")
        else:
            print("probably went well")
        pygame.quit()
        calibrator.leave_calibration_mode()

    def show_gaze_position(self):

        self.eye_tracker.subscribe_to(tb.EYETRACKER_GAZE_DATA, TobiiSetUp.gaze_data_callback, as_dictionary=False)
        pygame.init()
        self.screen = pygame.display.set_mode((self.w, self.h), FULLSCREEN)
        while True:
            self.screen.fill((0, 0, 0))
            if not TobiiSetUp.x or not TobiiSetUp.y:
                continue
            x = int(np.mean(TobiiSetUp.x) * self.w)
            y = int(np.mean(TobiiSetUp.y) * self.h)
            if (not 0 <= x <= self.w) or (not 0 <= y <= self.h):
                continue

            pygame.draw.circle(self.screen, color=(255, 255, 255), center=(x, y), radius=10)
            # win32api.SetCursorPos((x, y))
            pygame.display.update()
            # print(x, y)

            for event in pygame.event.get():
                if event.type == QUIT or event.type == pygame.KEYDOWN:
                    pygame.quit()
                    break
        print("quit")
        self.eye_tracker.unsubscribe_from(tb.EYETRACKER_GAZE_DATA, TobiiSetUp.gaze_data_callback)

    @staticmethod
    def gaze_data_callback(gaze_data):
        xl, yl = gaze_data.left_eye.gaze_point.position_on_display_area
        xr, yr = gaze_data.right_eye.gaze_point.position_on_display_area
        if np.isnan(xl) or np.isnan(yl) or np.isnan(xr) or np.isnan(yr):
            return
        TobiiSetUp.x.append((xl + xr)/2)
        TobiiSetUp.y.append((yl + yr)/2)

        if len(TobiiSetUp.x) > 50:
            del TobiiSetUp.x[0]
            del TobiiSetUp.y[0]

    def __get_calibration_points(self):
        x1, y1 = int(self.w * 0.1), int(self.h * 0.1)
        # print("upper left: ", x1, y1)

        x2, y2 = int(self.w * 0.1), int(self.h * 0.9)
        # print("lower left: ", x2, y2)

        x3, y3 = int(self.w * 0.9), int(self.h * 0.1)
        # print("upper right: ", x3, y3)

        x4, y4 = int(self.w * 0.9), int(self.h * 0.9)
        # print("lower right:", x4, y4)

        x5, y5 = int(self.w * 0.5), int(self.h * 0.5)
        # print("center:", x5, y5)

        calibration_points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5)]

        return calibration_points


if __name__ == "__main__":
    test = TobiiSetUp()
    # test.calibrate()
    test.show_gaze_position()