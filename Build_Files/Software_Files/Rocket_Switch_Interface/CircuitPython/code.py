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

# === Load config.py ===
try:
    import config
    raw_config = config.CONFIG.get("modes", {})
    print("Config loaded from config.py")
except (ImportError, AttributeError):
    print("config.py not found or invalid — using defaults")
    raw_config = {
        "0": {"rota": {"type": "keyboard", "keys": ["TAB"]},
              "switch": {"type": "keyboard", "keys": ["ENTER"]}},
        "1": {"rota": {"type": "consumer", "code": "SCAN_NEXT_TRACK"},
              "switch": {"type": "consumer", "code": "PLAY_PAUSE"}},
        "2": {"rota": {"type": "mouse", "button": "RIGHT_BUTTON"},
              "switch": {"type": "mouse", "button": "LEFT_BUTTON"}},
    }

# === LED colors per mode ===
MODE_COLORS = [
    (0, 0, 255),       # Blue
    (0, 255, 0),       # Green
    (255, 0, 255),     # Magenta
    (255, 200, 0),     # Yellow
]

# === HID Hardware init ===
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

rota = digitalio.DigitalInOut(board.ROTA)
rota.direction = digitalio.Direction.INPUT
rota.pull = digitalio.Pull.UP

switch = digitalio.DigitalInOut(board.SWITCH)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# === HID logic ===
def do_action(action, is_press):
    t = action.get("type")
    if t == "keyboard":
        codes = [getattr(Keycode, k, None) for k in action.get("keys", [])]
        codes = [c for c in codes if c is not None]
        if is_press:
            kbd.press(*codes)
        else:
            kbd.release_all()
    elif t == "consumer" and is_press:
        code = getattr(ConsumerControlCode, action.get("code", ""), None)
        if code: cc.send(code)
    elif t == "mouse" and is_press:
        btn_map = {"LEFT_BUTTON": Mouse.LEFT_BUTTON, "RIGHT_BUTTON": Mouse.RIGHT_BUTTON, "MIDDLE_BUTTON": Mouse.MIDDLE_BUTTON}
        btn = btn_map.get(action.get("button", ""), Mouse.LEFT_BUTTON)
        mouse.click(btn)

# === Main State & Loop ===
mode = 0
rota_pressed = False
switch_pressed = False
pixel.fill(MODE_COLORS[mode])

while True:
    r_state = not rota.value
    s_state = not switch.value

    # Cycle Mode (Both Pressed)
    if r_state and s_state and not (rota_pressed and switch_pressed):
        mode = (mode + 1) % 4
        pixel.fill(MODE_COLORS[mode])
        time.sleep(0.4)
        continue

    # Handle ROTA
    if r_state != rota_pressed:
        action = raw_config.get(str(mode), {}).get("rota", {})
        do_action(action, r_state)
        rota_pressed = r_state

    # Handle SWITCH
    if s_state != switch_pressed:
        action = raw_config.get(str(mode), {}).get("switch", {})
        do_action(action, s_state)
        switch_pressed = s_state

    time.sleep(0.01)