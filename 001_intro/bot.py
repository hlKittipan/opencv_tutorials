import cv2 as cv
import numpy as np
import os
import sys
import pyautogui
from pywinauto.application import Application

# def winEnumHandler(hwnd, ctx):
#     if win32gui.IsWindowVisible(hwnd):
#         print(hex(hwnd), win32gui.GetWindowText(hwnd))
#
#
# win32gui.EnumWindows(winEnumHandler, None)


def getWindowsCapture(window_name, windows_name=None):
    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    # windows_name = win32gui.FindWindow(None, window_name)
    if not windows_name:
        raise Exception('Window not found: {}'.format(window_name))
    # get the window size
    # window_rect = win32gui.GetWindowRect(windows_name)
    # w = window_rect[2] - window_rect[0]
    # h = window_rect[3] - window_rect[1]

    # wDC = win32gui.GetWindowDC(windows_name)
    # dcObj = win32ui.CreateDCFromHandle(wDC)
    # cDC = dcObj.CreateCompatibleDC()
    # dataBitMap = win32ui.CreateBitmap()
    # dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    # cDC.SelectObject(dataBitMap)
    # cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

    # convert the raw data into a format opencv can read
    # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
    # signedIntsArray = dataBitMap.GetBitmapBits(True)
    # img = np.fromstring(signedIntsArray, dtype='uint8')
    # img.shape = (h, w, 4)
    # myScreenshot = pyautogui.screenshot()
    # myScreenshot = np.array(img)
    # print(myScreenshot)
    # free resources
    # dcObj.DeleteDC()
    # cDC.DeleteDC()
    # win32gui.ReleaseDC(window_name, wDC)
    # win32gui.DeleteObject(dataBitMap.GetHandle())
    # cv.imshow('Computer Vision', myScreenshot)

    # drop the alpha channel, or cv.matchTemplate() will throw an error like:
    #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type()
    #   && _img.dims() <= 2 in function 'cv::matchTemplate'
    # img = img[..., :3]

    # make image C_CONTIGUOUS to avoid errors that look like:
    #   File ... in draw_rectangles
    #   TypeError: an integer is required (got type tuple)
    # see the discussion here:
    # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
    # img = np.ascontiguousarray(img)

    print('done')


# def callback(hwnd, strings):
#     if win32gui.IsWindowVisible(hwnd):
#         window_title = win32gui.GetWindowText(hwnd)
#         left, top, right, bottom = win32gui.GetWindowRect(hwnd)
#         if window_title and right - left and bottom - top:
#             strings.append('0x{:08x}: "{}"'.format(hwnd, window_title))
#     return True


def main():
    win_list = []  # list of strings containing win handles and window titles
    # win32gui.EnumWindows(callback, win_list)  # populate list
    # app = Application().start("notepad.exe")
    #
    # app.UntitledNotepad.menu_select("Help->About Notepad")
    # app.AboutNotepad.OK.click()
    # app.UntitledNotepad.Edit.type_keys("pywinauto Works!", with_spaces=True)

    for window in win_list:  # print results
        print(window)

    getWindowsCapture('opencv_tutorials – bot.py')
    sys.exit(0)


if __name__ == '__main__':
    main()
