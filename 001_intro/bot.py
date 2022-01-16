import numpy as np
import os
import sys
import pyautogui
import pywinauto
import ctypes
import win32gui
from PIL import ImageGrab
import cv2
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from skimage import color, data


def main():
    print('main')
    win_list = []  # list of strings containing win handles and window titles
    # win32gui.EnumWindows(callback, win_list)  # populate list
    # win_list = pywinauto.findwindows.enum_windows()
    # win_list = pywinauto.findwindows.find_windows(best_match='Bombcrypto - Google Chrome')
    app = pywinauto.Application().connect(title_re=".*Bombcrypto")
    hwin = app.top_window()
    hwin.set_focus()

    window_title = hwin.window_text()
    print(window_title)
    hwnd = win32gui.FindWindow(None, window_title)
    dimensions = win32gui.GetWindowRect(hwnd)
    print(dimensions)
    windows = pywinauto.Desktop(backend="uia").windows()
    print([w.window_text() for w in windows])
    # rect = ctypes.wintypes.RECT()
    # DWMWA_EXTENDED_FRAME_BOUNDS = 9
    # ctypes.windll.dwmapi.DwmGetWindowAttribute(
    #     ctypes.wintypes.HWND(win32gui.FindWindow(None, window_title)),
    #     ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
    #     ctypes.byref(rect),
    #     ctypes.sizeof(rect)
    # )
    # print(rect)
    image = ImageGrab.grab(bbox=(10, 10, 1060, 728))
    image.show()
    # print([w.window_text() for w in win_list])

    # for window in win_list:  # print results
    #     print(window)
    # os.system("pause")

    # getWindowsCapture('opencv_tutorials – bot.py')
    # sys.exit(0)


MIN_MATCH_COUNT = 10


if __name__ == '__main__':
    image_path = sys.path[0] + '/img/board_game.png'
    app = pywinauto.Application().connect(title_re=".*Bombcrypto")
    hwin = app.top_window()
    hwin.set_focus()

    window_title = hwin.window_text()
    hwnd = win32gui.FindWindow(None, window_title)
    dimensions = win32gui.GetWindowRect(hwnd)
    print(dimensions)
    image = ImageGrab.grab(bbox=dimensions)

    img1 = cv2.imread(sys.path[0] + '/img/treasure_hunt.png', 0)
    img2 = np.array(image)

    # Initiate SIFT detector
    sift = cv2.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()
        h, w = img1.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]
                         ).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        print(dst[0])

        img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.IMREAD_COLOR)
        cv2.imshow('image', img2)

    else:
        print("Not enough matches are found - %d/%d" %
              (len(good), MIN_MATCH_COUNT))
        matchesMask = None
    draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                       singlePointColor=None,
                       matchesMask=matchesMask,  # draw only inliers
                       flags=2)
    img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)

    # hunt = cv2.imread(image_path, cv2.IMREAD_COLOR)
    cv2.imshow('result', img3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # main()
