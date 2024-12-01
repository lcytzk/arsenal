import subprocess

import pyperclip
import Quartz

import pyautogui


def write_to_clipboard(output):
    pyperclip.copy(output)


def read_from_clipboard():
    return pyperclip.paste()


def scroll_pixel(pixel):
    scrollWheelEvent = Quartz.CGEventCreateScrollWheelEvent(
        None,  # no source
        Quartz.kCGScrollEventUnitPixel,  # units
        1,  # wheelCount (number of dimensions)
        pixel,
    )  # vertical movement
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, scrollWheelEvent)


def hotkey(a, b):
    pyautogui.keyDown(a)
    pyautogui.press(b)
    pyautogui.keyUp(a)


def get_text_from_html(p1, p2) -> str:
    pyautogui.moveTo(*p1)
    pyautogui.dragTo(*p2, button="left", duration=0.5)
    hotkey("command", "c")
    pyautogui.sleep(0.5)
    return read_from_clipboard().strip()
