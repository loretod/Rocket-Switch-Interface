import board
import digitalio
import neopixel
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse

# === CUSTOMIZE YOUR KEYS HERE ===
ROTA_KEY = Keycode.TAB      # Change to any Keycode (e.g., Keycode.A, Keycode.SPACE)
SWITCH_KEY = Keycode.ENTER  # Change to any Keycode (e.g., Keycode.B, Keycode.ENTER)
# =================================

# Initialize hardware
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3)
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

# Setup buttons
rota = digitalio.DigitalInOut(board.ROTA)
rota.direction = digitalio.Direction.INPUT
rota.pull = digitalio.Pull.UP

switch = digitalio.DigitalInOut(board.SWITCH)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# State tracking
rota_pressed = False
switch_pressed = False
mode = 0  # 0=arrows, 1=media, 2=mouse

# Set initial color
pixel.fill((0, 0, 255))  # Blue

def handle_mode_switch():
    global mode
    mode = (mode + 1) % 3
    if mode == 0:
        pixel.fill((0, 0, 255))  # Blue - arrows
    elif mode == 1:
        pixel.fill((0, 255, 0))  # Green - media
    else:
        pixel.fill((255, 0, 255))  # Magenta - mouse

while True:
    rota_state = not rota.value
    switch_state = not switch.value

    # Check for mode switch (both pressed)
    if rota_state and switch_state and not (rota_pressed and switch_pressed):
        handle_mode_switch()
        rota_pressed = True
        switch_pressed = True
        time.sleep(0.3)  # Delay to prevent accidental actions after mode switch
        continue

    # ROTA button
    if rota_state and not rota_pressed:
        if mode == 0:
            kbd.press(ROTA_KEY)
        elif mode == 1:
            cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)
        else:  # mode == 2
            mouse.click(Mouse.RIGHT_BUTTON)
        rota_pressed = True
    elif not rota_state and rota_pressed:
        if mode == 0:
            kbd.release(ROTA_KEY)
        rota_pressed = False

    # SWITCH button
    if switch_state and not switch_pressed:
        if mode == 0:
            kbd.press(SWITCH_KEY)
        elif mode == 1:
            cc.send(ConsumerControlCode.PLAY_PAUSE)
        else:  # mode == 2
            mouse.click(Mouse.LEFT_BUTTON)
        switch_pressed = True
    elif not switch_state and switch_pressed:
        if mode == 0:
            kbd.release(SWITCH_KEY)
        switch_pressed = False

    time.sleep(0.005)
