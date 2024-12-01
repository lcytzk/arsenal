import Quartz.CoreGraphics as CG
from Quartz import *


def xy(event):
    location = CG.CGEventGetLocation(event)
    x, y = location.x, location.y
    return x, y


def mouse_event_callback(proxy, type_, event, refcon):
    # 判断事件类型
    if type_ == CG.kCGEventLeftMouseDown:
        print(f"Left Mouse Button Pressed {xy(event)}")
    elif type_ == CG.kCGEventLeftMouseUp:
        print("Left Mouse Button Released")
    elif type_ == CG.kCGEventRightMouseDown:
        print("Right Mouse Button Pressed")
    elif type_ == CG.kCGEventRightMouseUp:
        print("Right Mouse Button Released")
    # elif type_ == CG.kCGEventMouseMoved:
    #     print("Mouse Moved")
    elif type_ == CG.kCGEventScrollWheel:
        print("Scroll Wheel Moved")
    return event


tap = CGEventTapCreate(
    kCGSessionEventTap,
    kCGHeadInsertEventTap,
    kCGEventTapOptionDefault,
    CGEventMaskBit(kCGEventMouseMoved)
    | CGEventMaskBit(kCGEventLeftMouseDown)
    | CGEventMaskBit(kCGEventLeftMouseUp)
    | CGEventMaskBit(kCGEventRightMouseDown)
    | CGEventMaskBit(kCGEventRightMouseUp)
    | CGEventMaskBit(kCGEventOtherMouseDown)
    | CGEventMaskBit(kCGEventOtherMouseUp),
    mouse_event_callback,
    None,
)

loopsource = CFMachPortCreateRunLoopSource(None, tap, 0)
loop = CFRunLoopGetCurrent()
CFRunLoopAddSource(loop, loopsource, kCFRunLoopDefaultMode)
CGEventTapEnable(tap, True)

while True:
    CFRunLoopRunInMode(kCFRunLoopDefaultMode, 5, False)
