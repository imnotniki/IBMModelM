import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Configure keyboard pins
KB_CLOCK = board.IO1  # Clock pin
KB_DATA = board.IO2   # Data pin

# Initialize pins
clock_pin = digitalio.DigitalInOut(KB_CLOCK)
data_pin = digitalio.DigitalInOut(KB_DATA)
clock_pin.direction = digitalio.Direction.INPUT
data_pin.direction = digitalio.Direction.INPUT
clock_pin.pull = digitalio.Pull.UP
data_pin.pull = digitalio.Pull.UP

# Initialize HID keyboard
keyboard = Keyboard(usb_hid.devices)

def read_keyboard_byte():
    """Read one byte from Model M keyboard"""
    data = 0
    bit_count = 0
    
    # Wait for start bit (clock falling edge)
    while clock_pin.value:
        pass
    
    # Verify start bit (should be 0)
    if data_pin.value:
        return None
        
    # Wait for clock to rise
    while not clock_pin.value:
        pass
        
    # Read 8 data bits
    for i in range(8):
        # Wait for clock falling edge
        while clock_pin.value:
            pass
            
        # Read data bit (LSB first)
        if data_pin.value:
            data |= (1 << i)
            
        # Wait for clock rising edge
        while not clock_pin.value:
            pass
            
    # Wait for parity bit
    while clock_pin.value:
        pass
    while not clock_pin.value:
        pass
        
    # Wait for stop bit
    while clock_pin.value:
        pass
    while not clock_pin.value:
        pass
        
    return data

# Scancode to HID keycode mapping (partial - expand as needed)
SCANCODE_TO_HID = {
    0x1C: 'a', 0x32: 'b'
}

def process_scancode(code):
    """Convert scancode to character or HID key"""
    if code == 0xF0:  # Key release code
        return None
    if code in SCANCODE_TO_HID:
        return SCANCODE_TO_HID[code]
    return None  # Return None if code isn't mapped

# Main loop
print("Keyboard ready. Waiting for input...")
last_code = None

while True:
    code = read_keyboard_byte()
    if code is not None:
        if code == 0xF0:  # Key release
            last_code = code
        elif last_code == 0xF0:  # Key release complete
            last_code = None
        else:  # Key press
            print(f"scancode: 0x{code:02x}")
    
    time.sleep(0.001)  # Small delay to prevent tight loop

