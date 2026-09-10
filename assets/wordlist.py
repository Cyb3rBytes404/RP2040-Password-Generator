# ============================================================
# wordlist.py
#
# Word lists used to build passwords. Kept in its own file so the
# words can be edited/expanded without touching the main program
# logic in main.py.
#
# main.py imports this file with:
#     from wordlist import adjectives, animals, symbols
# ============================================================

adjectives = [
    "Happy",
    "Purple",
    "Fuzzy",
    "Brave",
    "Silly",
    "Turbo",
    "Mighty",
    "Crazy",
    "Lucky",
    "Fluffy",
    "Sneaky",
    "Super",
    "Cosmic",
    "Rocket",
    "Ninja",
    "Magic",
    "Electric",
    "Awesome",
    "Clever",
    "Wild"
]


animals = [
    "Dino",
    "Panda",
    "Tiger",
    "Dragon",
    "Koala",
    "Penguin",
    "Fox",
    "Monkey",
    "Shark",
    "Otter",
    "Lion",
    "Wolf",
    "Eagle",
    "Gecko",
    "Llama",
    "Frog",
    "Kitten",
    "Falcon",
    "Turtle",
    "Raccoon"
]


# Not currently used in generate_password() (dropped to help keep
# passwords under the 16-character OLED width limit), but left here
# in case you want to bring it back in a future word combination.
places = [
    "Planet",
    "Castle",
    "Jungle",
    "Galaxy",
    "Volcano",
    "Island",
    "Moon",
    "Space",
    "Mountain",
    "Ocean",
    "Rocket",
    "Fortress"
]


# Symbols for stronger passwords
symbols = "!@#$%&*"
