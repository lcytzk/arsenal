from pynput import keyboard, mouse


def on_move(x, y):
    pass
    # print("Pointer moved to {0}".format((x, y)))


def on_click(x, y, button, pressed):
    # print("{0} at {1}".format("Pressed" if pressed else "Released", (x, y)))
    if pressed:
        print(f"({x}, {y}),")
    # if not pressed:
    #     # Stop listener
    #     return False


def on_scroll(x, y, dx, dy):
    print("Scrolled {0} at {1}".format("down" if dy < 0 else "up", (x, y)))


m_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)


def on_press(key):
    try:
        print("alphanumeric key {0} pressed".format(key.char))
    except AttributeError:
        print("special key {0} pressed".format(key))


def on_release(key):
    print("{0} released".format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        m_listener.stop()
        return False


k_listener = keyboard.Listener(on_press=on_press, on_release=on_release)


def run_mouse_listener():
    m_listener.start()
    m_listener.join()


def run_keyboard_listener():
    k_listener.start()
    k_listener.join()


from concurrent.futures import ThreadPoolExecutor

# Create thread pool and submit the mouse listener
with ThreadPoolExecutor(max_workers=2) as executor:
    future = executor.submit(run_mouse_listener)
    future2 = executor.submit(run_keyboard_listener)

    future.result()
    future2.result()
