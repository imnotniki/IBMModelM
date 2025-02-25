import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Configure keyboard pins
KB_CLOCK = board.IO4  # Clock pin
KB_DATA = board.IO5   # Data pin

# Initialize pins
clock_pin = digitalio.DigitalInOut(KB_CLOCK)
data_pin = digitalio.DigitalInOut(KB_DATA)
clock_pin.direction = digitalio.Direction.INPUT
data_pin.direction = digitalio.Direction.INPUT
clock_pin.pull = digitalio.Pull.UP
data_pin.pull = digitalio.Pull.UP

# Initialize HID keyboard
keyboard = Keyboard(usb_hid.devices)

# Scancode to HID keycode mapping for German keyboard layout
SCANCODE_TO_HID = {
    0x1C: Keycode.A, 0x32: Keycode.B, 0x21: Keycode.C, 0x23: Keycode.D, 0x24: Keycode.E,
    0x2B: Keycode.F, 0x34: Keycode.G, 0x33: Keycode.H, 0x43: Keycode.I, 0x3B: Keycode.J,
    0x42: Keycode.K, 0x4B: Keycode.L, 0x3A: Keycode.M, 0x31: Keycode.N, 0x44: Keycode.O,
    0x4D: Keycode.P, 0x15: Keycode.Q, 0x2D: Keycode.R, 0x1B: Keycode.S, 0x2C: Keycode.T,
    0x3C: Keycode.U, 0x2A: Keycode.V, 0x1D: Keycode.W, 0x22: Keycode.X, 0x35: Keycode.Y,
    0x1A: Keycode.Z, 0x45: Keycode.ZERO, 0x16: Keycode.ONE, 0x1E: Keycode.TWO,
    0x26: Keycode.THREE, 0x25: Keycode.FOUR, 0x2E: Keycode.FIVE, 0x36: Keycode.SIX,
    0x3D: Keycode.SEVEN, 0x3E: Keycode.EIGHT, 0x46: Keycode.NINE, 0x0E: Keycode.GRAVE_ACCENT,
    0x4E: Keycode.MINUS, 0x55: Keycode.EQUALS, 0x5C: Keycode.BACKSLASH, 0x66: Keycode.BACKSPACE,
    0x29: Keycode.SPACE, 0x0D: Keycode.TAB, 0x14: Keycode.CAPS_LOCK, 0x12: Keycode.SHIFT,
    0x11: Keycode.CONTROL, 0x8B: Keycode.GUI, 0x19: Keycode.ALT, 0x59: Keycode.SHIFT,
    0x58: Keycode.CONTROL, 0x8C: Keycode.GUI, 0x39: Keycode.ALT, 0x8D: Keycode.APPLICATION,
    0x5A: Keycode.ENTER, 0x08: Keycode.ESCAPE, 0x07: Keycode.F1, 0x0F: Keycode.F2,
    0x17: Keycode.F3, 0x1F: Keycode.F4, 0x27: Keycode.F5, 0x2F: Keycode.F6,
    0x37: Keycode.F7, 0x3F: Keycode.F8, 0x47: Keycode.F9, 0x4F: Keycode.F10,
    0x56: Keycode.F11, 0x5E: Keycode.F12, 0x57: Keycode.PRINT_SCREEN, 0x5F: Keycode.SCROLL_LOCK,
    0x62: Keycode.PAUSE, 0x54: Keycode.LEFT_BRACKET, 0x5B: Keycode.RIGHT_BRACKET,
    0x4C: Keycode.SEMICOLON, 0x52: Keycode.QUOTE, 0x41: Keycode.COMMA, 0x49: Keycode.PERIOD,
    0x4A: Keycode.FORWARD_SLASH, 0x67: Keycode.INSERT, 0x6E: Keycode.HOME, 0x6F: Keycode.PAGE_UP,
    0x64: Keycode.DELETE, 0x65: Keycode.END, 0x6D: Keycode.PAGE_DOWN, 0x63: Keycode.UP_ARROW,
    0x61: Keycode.LEFT_ARROW, 0x60: Keycode.DOWN_ARROW, 0x6A: Keycode.RIGHT_ARROW,
    0x76: Keycode.KEYPAD_NUMLOCK, 0x4A: Keycode.KEYPAD_FORWARD_SLASH, 0x7E: Keycode.KEYPAD_ASTERISK,
    0x4E: Keycode.KEYPAD_MINUS, 0x7C: Keycode.KEYPAD_PLUS, 0x79: Keycode.KEYPAD_ENTER,
    0x71: Keycode.KEYPAD_PERIOD, 0x70: Keycode.KEYPAD_ZERO, 0x69: Keycode.KEYPAD_ONE,
    0x72: Keycode.KEYPAD_TWO, 0x7A: Keycode.KEYPAD_THREE, 0x6B: Keycode.KEYPAD_FOUR,
    0x73: Keycode.KEYPAD_FIVE, 0x74: Keycode.KEYPAD_SIX, 0x6C: Keycode.KEYPAD_SEVEN,
    0x75: Keycode.KEYPAD_EIGHT, 0x7D: Keycode.KEYPAD_NINE
}

def read_keyboard_byte():
    """Read one byte from PS/2 keyboard"""
    data = 0
    while clock_pin.value:
        pass
    if data_pin.value:
        return None
    while not clock_pin.value:
        pass
    for i in range(8):
        while clock_pin.value:
            pass
        if data_pin.value:
            data |= (1 << i)
        while not clock_pin.value:
            pass
    return data

print("Keyboard ready. Waiting for input...")
last_code = None

while True:
    code = read_keyboard_byte()
    if code is not None:
        if code == 0xF0:
            last_code = code
        elif last_code == 0xF0:
            last_code = None
        elif code in SCANCODE_TO_HID:
            keyboard.send(SCANCODE_TO_HID[code])
            print(f"Pressed: {SCANCODE_TO_HID[code]}")
    time.sleep(0.001)
