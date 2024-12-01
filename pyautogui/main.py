import os
import subprocess
import time

import pyautogui
from util import (
    get_text_from_html,
    hotkey,
    read_from_clipboard,
    scroll_pixel,
    write_to_clipboard,
)

pyautogui.PAUSE = 0.2
time.sleep(3)
print("start")

# left, right, splitter (1463.02734375, 584.5625)
# pixel 1299 * ????

SP = (1463.63671875, 544.0703125)

VIDEO_NUM_P = [
    (1109.390625, 282.171875),
    (1169.75390625, 281.41796875),
]

TITLE_P = [
    (240.390625, 665.89453125),
    (900.390625, 667.59375),
]
V2 = (1215.21484375, 286.0625)
SLIDES_P = [
    (1351.234375, 283.0078125),
    (1385.44140625, 163.87109375),
    (1353.3828125, 205.5546875),
    (1373.30078125, 114.57421875),
]

DOWNLOAD_V_P = [
    (454.0234375, 24.65625),
    (460.94140625, 94.70703125),
    (511.76953125, 223.1328125),
]

FIRST_VIDEO_P = (1265.81640625, 362.921875)

VIDEO_CARD_HEIGHT = 112
CLEAN_NET_P = (1514.81640625, 91.11328125)
SUBTITLE_P = [
    (1551.70703125, 404.42578125),
    (1441.27734375, 520.51171875),
    (1331.03515625, 528.015625),
]


def scroll_one_video():
    scroll_pixel(-VIDEO_CARD_HEIGHT)


def get_video_num():
    txt = get_text_from_html(VIDEO_NUM_P[0], VIDEO_NUM_P[1])
    return int(txt.split()[0])


def download_slides():
    pyautogui.click(*SLIDES_P[0])
    pyautogui.sleep(10)
    pyautogui.click(*SLIDES_P[1])
    pyautogui.click(*SLIDES_P[2])
    pyautogui.click(*SLIDES_P[3])


def download_subtitle(title):
    pyautogui.rightClick(*SUBTITLE_P[0])
    pyautogui.click(SUBTITLE_P[1])
    pyautogui.click(SUBTITLE_P[2])
    pyautogui.sleep(1)
    download_file(read_from_clipboard(), f"{title}.vtt")


def download_file(url, name):
    curl_cmd = f"curl '{url}' > {name}"
    print(curl_cmd)
    subprocess.call(curl_cmd, shell=True)


def download_video_and_subtitle():
    pass


def get_title():
    title = get_text_from_html(*TITLE_P)
    return title.replace(" ", "_")


def rename_dowloaded_video(name: str):
    write_to_clipboard(name)
    for _ in range(2):
        try:
            x, y = pyautogui.locateCenterOnScreen("edit.ico")
            pyautogui.moveTo(x / 2, y / 2)
            pyautogui.doubleClick()
            hotkey("command", "a")
            hotkey("command", "v")
            pyautogui.press("enter")
            return
        except:
            print(f" failed {time.time()}")


def download_one_video(title):
    for p in DOWNLOAD_V_P:
        pyautogui.moveTo(*p)
        pyautogui.sleep(0.2)
        pyautogui.click()
    time.sleep(0.2)
    rename_dowloaded_video(title)


def locate_video(idx):
    x = FIRST_VIDEO_P[0]
    if idx < 6:
        y = FIRST_VIDEO_P[1] + (idx * VIDEO_CARD_HEIGHT)
        pyautogui.moveTo(x=x, y=y)
    else:
        y = FIRST_VIDEO_P[1] + (5 * VIDEO_CARD_HEIGHT)
        pyautogui.moveTo(x=x, y=y)
        n = idx - 5
        for _ in range(n):
            scroll_one_video()


def clean_net():
    pyautogui.click(*CLEAN_NET_P)


def download_videos_one_page():
    # download slides once
    download_slides()
    for i in range(get_video_num()):
        # reset to the top
        scroll_pixel(VIDEO_CARD_HEIGHT * 10)
        clean_net()
        # load video page
        locate_video(i)
        pyautogui.click()
        # pyautogui.sleep(1.5)
        # time.sleep(1.5)
        # get title
        title = get_title()
        # pyautogui.sleep(0.5)
        # # download subtitle
        download_subtitle(os.path.join("video", title))
        # # download video
        download_one_video(title)
        hotkey("ctrl", "tab")
        time.sleep(5)


download_videos_one_page()
