import cv2 as cv
import numpy as np
import os
import numpy as np
import sys
import win32gui, win32ui, win32con


# def winEnumHandler(hwnd, ctx):
#     if win32gui.IsWindowVisible(hwnd):
#         print(hex(hwnd), win32gui.GetWindowText(hwnd))
#
#
# win32gui.EnumWindows(winEnumHandler, None)


def getWindowsCapture(window_name):
    windows_name = win32gui.FindWindow(None, window_name)
    if not windows_name:
        raise Exception('Window not found: {}'.format(window_name))
    # get the window size
    window_rect = win32gui.GetWindowRect(windows_name)
    print(window_rect)


def callback(hwnd, strings):
    if win32gui.IsWindowVisible(hwnd):
        window_title = win32gui.GetWindowText(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if window_title and right - left and bottom - top:
            strings.append('0x{:08x}: "{}"'.format(hwnd, window_title))
    return True


def main():
    win_list = []  # list of strings containing win handles and window titles
    win32gui.EnumWindows(callback, win_list)  # populate list
    getWindowsCapture('Administrator: Command Prompt')

    for window in win_list:  # print results
        print(window)

    sys.exit(0)


if __name__ == '__main__':
    main()
