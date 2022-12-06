import keyboard

def print_pressed_keys(e):
    print(e.name)


print(keyboard.hook(print_pressed_keys))
keyboard.hook(print_pressed_keys)
keyboard.wait()
