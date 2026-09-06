# ============================================================
# led_effects.py
#
# LED animations for the WS2812B strip. Kept in its own file so new
# animations can be added, or the active one swapped, without
# touching main.py.
#
# HOW TO CHOOSE WHICH ANIMATION RUNS:
# Change the ACTIVE_EFFECT string below to the name of any key in
# the EFFECTS dictionary near the bottom of this file.
#
# main.py calls this module with:
#     import led_effects
#     interrupted = led_effects.run_selected_effect(np, NUM_LEDS, button)
# ============================================================

import time


def apply_brightness(color, brightness):

    return (
        int(color[0] * brightness),
        int(color[1] * brightness),
        int(color[2] * brightness)
    )


def clear_leds(np):

    np.fill((0, 0, 0))

    np.write()


# ------------------------------------------------------------
# EFFECT: bouncing
# A single pixel bounces back and forth along the strip, cycling
# through red, blue, and green.
# ------------------------------------------------------------
def bouncing_effect(np, num_leds, button):

    # Returns True if the animation was cut short by a new button
    # press, or False if it finished on its own without interruption.

    brightness = 0.20

    base_colors = [

        (255, 0, 0),      # Red
        (0, 0, 255),      # Blue
        (0, 255, 0)       # Green

    ]

    for base_color in base_colors:

        color = apply_brightness(
            base_color,
            brightness
        )

        for i in range(num_leds):

            if button.value() == 0:
                clear_leds(np)
                return True

            np.fill((0, 0, 0))

            np[i] = color

            np.write()

            time.sleep_ms(50)

        for i in range(num_leds - 2, -1, -1):

            if button.value() == 0:
                clear_leds(np)
                return True

            np.fill((0, 0, 0))

            np[i] = color

            np.write()

            time.sleep_ms(50)

    clear_leds(np)

    return False


# ------------------------------------------------------------
# EFFECT: solid_flash
# A simple alternative effect: the whole strip flashes a color a
# few times. Included as an example of a second animation you can
# switch to below.
# ------------------------------------------------------------
def solid_flash_effect(np, num_leds, button):

    brightness = 0.20

    color = apply_brightness((0, 255, 255), brightness)  # Cyan

    for _ in range(6):

        if button.value() == 0:
            clear_leds(np)
            return True

        np.fill(color)
        np.write()
        time.sleep_ms(150)

        if button.value() == 0:
            clear_leds(np)
            return True

        np.fill((0, 0, 0))
        np.write()
        time.sleep_ms(150)

    clear_leds(np)

    return False


# ------------------------------------------------------------
# Pick which effect runs when a new password is generated.
# Must match one of the keys in EFFECTS below.
# ------------------------------------------------------------
ACTIVE_EFFECT = "bouncing"


EFFECTS = {
    "bouncing": bouncing_effect,
    "solid_flash": solid_flash_effect,
}


def run_selected_effect(np, num_leds, button):

    effect_function = EFFECTS.get(ACTIVE_EFFECT, bouncing_effect)

    return effect_function(np, num_leds, button)
