import time

import pyautogui

pyautogui.PAUSE = 0.5
time.sleep(2)

mouse_positions = [
    # (458.5078125, 19.33984375),  # menu bar的插件位置
    # (473.73828125, 96.5078125),  # 需要的插件的具体位置
    # (448.69140625, 719.109375),  # 需要复制的课的名字，用来重命名文件
    (1061.3515625, 761.5078125),  # slides button
    (1694.78515625, 127.40625),  # 课件下载的setting按键
    (1643.15234375, 163.0078125),  # setting内的下载位置，课件的名字存储的正确
]


def download_slides():
    ps = [
        (1061.3515625, 761.5078125),  # slides button
        (1694.78515625, 127.40625),  # 课件下载的setting按键
        (1643.15234375, 163.0078125),  # setting内的下载位置，课件的名字存储的正确
    ]
    pyautogui.moveTo(1061.3515625, 761.5078125)
    pyautogui.click()
    pyautogui.sleep(3)
    pyautogui.moveTo(1694.78515625, 127.40625)
    pyautogui.click()
    pyautogui.moveTo(1643.15234375, 163.0078125)
    pyautogui.click()


# def open_page(url):
#     write_to_clipboard(url)
#     hotkey("option", "space")
#     hotkey("command", "v")
#     pyautogui.press("enter")


def download_video():
    pass


def download_subtitle():
    pass


# 1. call this function when you in course vdeo page
def download_course():
    # 1. download video, because it takes time
    download_video()
    # 2. download slides
    download_slides()
    # 3. download subtitle
    download_subtitle()


# screenWidth, screenHeight = (
#     pyautogui.size()
# )  # Returns two integers, the width and height of the screen. (The primary monitor, in multi-monitor setups.)
# currentMouseX, currentMouseY = (
#     pyautogui.position()
# )  # Returns two integers, the x and y of the mouse cursor's current position.


# for position in mouse_positions:
#     pyautogui.moveTo(*position)
#     pyautogui.click()


# pyautogui.moveTo(100, 150)  # Move the mouse to the x, y coordinates 100, 150.
# pyautogui.click()  # Click the mouse at its current location.
# pyautogui.click(200, 220)  # Click the mouse at the x, y coordinates 200, 220.
# pyautogui.move(
#     None, 10
# )  # Move mouse 10 pixels down, that is, move the mouse relative to its current position.
# pyautogui.doubleClick()  # Double click the mouse at the
# pyautogui.moveTo(
#     500, 500, duration=2, tween=pyautogui.easeInOutQuad
# )  # Use tweening/easing function to move mouse over 2 seconds.
# pyautogui.write(
#     "Hello world!", interval=0.25
# )  # Type with quarter-second pause in between each key.
# pyautogui.press("esc")  # Simulate pressing the Escape key.
# pyautogui.keyDown("shift")
# pyautogui.write(["left", "left", "left", "left", "left", "left"])
# pyautogui.keyUp("shift")
# pyautogui.hotkey("ctrl", "c")
