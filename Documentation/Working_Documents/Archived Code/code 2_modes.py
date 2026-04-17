# A program written by Claude AI and tweaked by Loreto Dumitrescu to create custom HID modes for the Makers Making Change Rocket Switch
# Press and hold button A for more than 2 seconds to switch modes
import board
import neopixel
import rotaryio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import digitalio
import time

# Setup the neopixel
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3

# Setup the buttons
button_rota = digitalio.DigitalInOut(board.ROTA)
button_rota.switch_to_input(pull=digitalio.Pull.UP)
button_switch = digitalio.DigitalInOut(board.SWITCH)
button_switch.switch_to_input(pull=digitalio.Pull.UP)

# Setup HID devices
keyboard = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# Mode variables
current_mode = 0
MODES = 3
mode_colors = [
    (0, 0, 255),    # Blue for mode 0
    (255, 165, 0),  # Orange for mode 1
    (0, 255, 0)     # Green for mode 2
]

# Button state tracking
last_rota_state = True
rota_press_time = 0
debounce_time = 0.05

# Mode 0: Sends Tab and Enter. Values may be modified as needed
def handle_mode_0():
    if not button_rota.value and time.monotonic() - debounce_time > 0.1:
        keyboard.press(Keycode.TAB)
        keyboard.release(Keycode.TAB)
    if not button_switch.value and time.monotonic() - debounce_time > 0.1:
        keyboard.press(Keycode.ENTER)
        keyboard.release(Keycode.ENTER)

# Mode 1: Sends dot and dash for Morse Code typing using GBoard
def handle_mode_1():
    if not button_rota.value and time.monotonic() - debounce_time > 0.1:
        keyboard.press(Keycode.PERIOD)
        keyboard.release(Keycode.PERIOD)
    if not button_switch.value and time.monotonic() - debounce_time > 0.1:
        keyboard.press(Keycode.MINUS)
        keyboard.release(Keycode.MINUS)

# Mode 2: Sends next song and play/ pause media control
def handle_mode_2():
    if not button_rota.value and time.monotonic() - debounce_time > 0.1:
        cc.send(ConsumerControlCode.PLAY_PAUSE)
    if not button_switch.value and time.monotonic() - debounce_time > 0.1:
        cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)

while True:
    # Check for mode change (ROTA long press)
    current_rota_state = button_rota.value
    
    if current_rota_state != last_rota_state:
        if not current_rota_state:  # Button pressed
            rota_press_time = time.monotonic()
        else:  # Button released
            # Change the number 2 below if you need a longer press time for mode switching
            if time.monotonic() - rota_press_time >= 2:
                current_mode = (current_mode + 1) % MODES
                pixel.fill(mode_colors[current_mode])
        last_rota_state = current_rota_state
    
    # Handle current mode
    if current_mode == 0:
        handle_mode_0()
    elif current_mode == 1:
        handle_mode_1()
    else:  # mode 2
        handle_mode_2()

    #Adjust the number here to control the speed of repeat rate
    time.sleep(0.2)  # Small delay to prevent overwhelming the system