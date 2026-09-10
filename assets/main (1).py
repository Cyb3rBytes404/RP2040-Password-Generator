from machine import Pin, I2C
import neopixel
import ssd1306
import time
import urandom

from wordlist import adjectives, animals, symbols
import led_effects


# ============================================================
# HARDWARE SETUP
# ============================================================

# WS2812B LEDs
LED_PIN = 9
NUM_LEDS = 30

np = neopixel.NeoPixel(
    Pin(LED_PIN),
    NUM_LEDS
)


# Button
# Button should connect GPIO7 to GND
button = Pin(
    7,
    Pin.IN,
    Pin.PULL_UP
)


# SSD1306 OLED
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

WIDTH = 128
HEIGHT = 32

oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

oled.write_cmd(0xA0)  # Segment remap: reversed (was 0xA1 by default)
oled.write_cmd(0xC0)  # COM output scan direction: reversed (was 0xC8 by default)


# Maximum password length. The default MicroPython font is 8px wide per
# character, and the display is 128px wide, so 16 characters is the most
# that will ever fit on one line without getting cut off.
MAX_PASSWORD_LENGTH = 16


# ============================================================
# RANDOM FUNCTIONS
# ============================================================

def random_number(maximum):

    return urandom.getrandbits(15) % maximum


def random_item(list_name):

    return list_name[
        random_number(len(list_name))
    ]


# ============================================================
# PASSWORD GENERATOR
# ============================================================

def generate_password():

    # Default strength = STRONG
    #
    # Combining a full adjective + animal can occasionally run close to
    # 16 characters once a number and symbol are added. Instead of
    # truncating mid-word (which can cut a word in half and look
    # broken), keep re-rolling the combination until one fits within
    # MAX_PASSWORD_LENGTH.

    for _ in range(200):

        adjective = random_item(adjectives)

        animal = random_item(animals)

        number = random_number(100)

        symbol = symbols[
            random_number(len(symbols))
        ]

        password = (adjective + animal + str(number) + symbol)

        if len(password) <= MAX_PASSWORD_LENGTH:

            return password

    # Extreme fallback (should practically never happen): hard-truncate.
    return password[:MAX_PASSWORD_LENGTH]


# ============================================================
# OLED FUNCTIONS
# ============================================================

def show_password(password):

    oled.fill(0)

    # Row 1 (y=0-8): the password itself. Guaranteed <= 16 chars, so it
    # always fits the full 128px width on its own line.
    oled.text(password, 0, 0)

    # Row 3 (y=16-24) and Row 4 (y=24-32): instructions, kept short
    # enough (<=16 chars) to fit on-screen.
    oled.text("Press Button", 0, 16)

    oled.text("For New Pass", 0, 24)

    oled.show()


def show_ready():

    oled.fill(0)

    oled.text("PASSWORD", 0, 0)

    oled.text("GENERATOR", 0, 8)

    oled.text("PRESS BUTTON", 0, 24)

    oled.show()


# ============================================================
# BUTTON DEBOUNCE
# ============================================================

def wait_for_button_release():

    while button.value() == 0:

        time.sleep_ms(15)


# ============================================================
# STARTUP
# ============================================================

led_effects.clear_leds(np)

show_ready()


print("CyberBytes404")
print("Password Generator")
print("================================")
print("Press GPIO7 to generate password")


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    # Button pressed?
    if button.value() == 0:

        # Small debounce delay
        time.sleep_ms(50)

        # Make sure it really is pressed
        if button.value() == 0:

            # Make sure the initial press has been released before we
            # start watching for a "second press" to interrupt the
            # animation, so the same press doesn't immediately trigger
            # an interrupt.
            wait_for_button_release()

            time.sleep_ms(50)

            keep_generating = True

            while keep_generating:

                # -----------------------------------------------
                # GENERATE PASSWORD
                # -----------------------------------------------

                password = generate_password()

                print("")
                print("New Password:")
                print(password)

                # -----------------------------------------------
                # DISPLAY PASSWORD
                # -----------------------------------------------

                show_password(password)

                # -----------------------------------------------
                # RUN LED ANIMATION (picked in led_effects.py)
                # -----------------------------------------------

                interrupted = led_effects.run_selected_effect(
                    np,
                    NUM_LEDS,
                    button
                )

                if interrupted:

                    # The button was pressed again mid-animation.
                    # Wait for that press to release, then loop back
                    # around and generate a fresh password right away.
                    wait_for_button_release()

                    time.sleep_ms(50)

                    keep_generating = True

                else:

                    # Animation finished on its own with no interruption.
                    keep_generating = False

            # Small pause before allowing another press
            time.sleep_ms(50)

    time.sleep_ms(20)
