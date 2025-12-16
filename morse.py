import machine
import time,network

# Morse code for digits 0-9
MORSE_CODE_DICT = {
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
}

# Pin configuration (onboard LED is usually on GPIO 2 for ESP32)
led = machine.Pin(2, machine.Pin.OUT)

# Morse timing
DOT_DURATION_MS = 200
DASH_DURATION_MS = DOT_DURATION_MS * 5
SYMBOL_PAUSE_MS = DOT_DURATION_MS*3
# LETTER_PAUSE_MS = DOT_DURATION_MS * 3 # Not strictly needed for a single digit

# Some boards have Inverted LED
INVERT=False

def blink_led(duration_ms):
    """Turns the LED on for a specified duration and then off."""
    if INVERT:
        led.off()
        time.sleep_ms(duration_ms)
        led.on()
    else:
        led.on()
        time.sleep_ms(duration_ms)
        led.off()

def morse_digit(digit):
    morse_sequence = MORSE_CODE_DICT.get(str(digit))
    if not morse_sequence:
        print(f"Error: No Morse code found for digit {digit}")
        return

    print(f"Morsing digit: {digit} -> {morse_sequence}")
    for symbol in morse_sequence:
        if symbol == '.':
            blink_led(DOT_DURATION_MS)
        elif symbol == '-':
            blink_led(DASH_DURATION_MS)
        time.sleep_ms(SYMBOL_PAUSE_MS)

def doit(number_to_morse):
    if INVERT:
        led.on()
        time.sleep(5)
    number=number_to_morse
    print("-" * 30)
    print(f"Configured digit to morse: {number}")
    print("-" * 30)
    iik=1000000
    while iik>number: iik=int(iik/10)
    while iik>0:
        morse_digit(int(number/iik))
        time.sleep(1)
        number=number%iik
        iik=int(iik/10)

def wifi():
    sta_if = network.WLAN(network.STA_IF)
    ifc=sta_if.ifconfig()
    print('network config:',ifc)
    n=int(ifc[0].split(".")[3])
    doit(n)
