import pywinauto
import win32gui
from PIL import ImageGrab
import cv2
import numpy as np
import os
import sys
from vision import Vision
import pyautogui

# load an empty Vision class
vision_limestone = Vision()
threshold = 0.8


def main():
    app = pywinauto.Application().connect(title_re=".*Bombcrypto")
    hwin = app.top_window()
    hwin.set_focus()

    window_title = hwin.window_text()
    hwnd = win32gui.FindWindow(None, window_title)
    dimensions = win32gui.GetWindowRect(hwnd)
    print(dimensions)

    image_path = sys.path[0] + '/img/board_game.png'

    # Real time matching
    image = ImageGrab.grab(bbox=dimensions)
    check_server_status(image)
    if os.path.isfile(image_path):
        print("File exists")
        board_game = cv2.imread(image_path)
        board_game = cv2.cvtColor(board_game, cv2.COLOR_BGR2GRAY)
        screen = np.array(image)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screen, board_game, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print('Best match top left position: %s' % str(max_loc))
        print('Best match confidence: %s' % max_val)
        if max_val >= threshold:
            print('Found bomb game.')
            # Get the size of the needle image. With OpenCV images, you can get the dimensions
            # via the shape property. It returns a tuple of the number of rows, columns, and
            # channels (if the image is color):
            object_draw = get_x_y_w_h(board_game, max_loc)
            print(object_draw)
            start_x = dimensions[0]
            start_y = dimensions[1]
            image_board_game = (start_x + object_draw[0], start_y + object_draw[1], object_draw[2], object_draw[3])
            # Draw a rectangle on our screenshot to highlight where we found the needle.
            # The line color can be set as an RGB tuple
            image = ImageGrab.grab(bbox=image_board_game)
            image = np.array(image)
            cv2.rectangle(image, (object_draw[0], object_draw[1]), (object_draw[2], object_draw[3]),
                          color=(0, 255, 0), thickness=2, lineType=cv2.LINE_4)

            # Detected Treasure Hunt
            object_draw = detected_treasure_hunt(image)
            cv2.rectangle(image, (object_draw[0], object_draw[1]), (object_draw[2], object_draw[3]),
                          color=(0, 255, 0), thickness=2, lineType=cv2.LINE_4)
            # You can view the processed screenshot like this:
            # cv.imshow('Result', haystack_img)
            # cv.waitKey()
            # Or you can save the results to a file.
            # imwrite() will smartly format our output image based on the extension we give it
            # https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html#gabbc7ef1aa2edfaa87772f1202d67e0ce
            cv2.imshow('result', image)
            while True:

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break


def check_server_status(image):
    image_path = sys.path[0] + '/img/server_loss.png'
    if os.path.isfile(image_path):
        board_game = cv2.imread(image_path)
        board_game = cv2.cvtColor(board_game, cv2.COLOR_RGB2GRAY)
        screen = np.array(image)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screen, board_game, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= threshold:
            print('Server loss')
            sys.exit(0)


def detected_treasure_hunt(image):
    image_path = sys.path[0] + '/img/treasure_hunt.png'
    hunt = cv2.imread(image_path)
    hunt = cv2.cvtColor(hunt, cv2.COLOR_BGR2GRAY)
    # image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(image, hunt, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        print('Found hunt.')
        return get_x_y_w_h(hunt, max_loc)
        # cv2.rectangle(image, (object_draw[0], object_draw[1]), (object_draw[2], object_draw[3]),
        #               color=(0, 255, 0), thickness=2, lineType=cv2.LINE_4)
    exit()


def get_x_y_w_h(item, max_loc):
    needle_w = item.shape[1]
    needle_h = item.shape[0]
    return max_loc[0], max_loc[1], max_loc[0] + needle_w, max_loc[1] + needle_h


if __name__ == '__main__':
    print(pyautogui.position())
    main()
