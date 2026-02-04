import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.matrix import MatrixScanner
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.rgb import RGB


keyboard = KMKKeyboard()


# KEY MATRIX (3 columns x 4 rows)

keyboard.matrix = MatrixScanner(
    row_pins=(
        board.GPIO2,  # R1
        board.GPIO3,  # R2
        board.GPIO4,  # R3
        board.GPIO5,  # R4
    ),
    col_pins=(
        board.GPIO6,  # C1
        board.GPIO7,  # C2
        board.GPIO8,  # C3
    ),
    columns_to_anodes=False, 
)


# LAYERS (MODES)

layers = Layers()
keyboard.modules.append(layers)


# ROTARY ENCODER

encoder = EncoderHandler()
encoder.pins = (
    (board.GPIO9, board.GPIO10),  
)

encoder.map = [
    (KC.VOLD, KC.VOLU),     # Mode 0
    (KC.LEFT, KC.RIGHT),   # Mode 1
    (KC.PGDN, KC.PGUP),    # Mode 2
]

keyboard.modules.append(encoder)


# SK6812 RGB LEDs (3 LEDs, single data pin)

rgb = RGB(
    pixel_pin=board.GPIO11,  
    num_pixels=3,
    hue_default=0,
    sat_default=255,
    val_default=80,
)

keyboard.extensions.append(rgb)


# MODE → LED COLOR INDICATION

def after_layer_change(layer):
    if layer == 0:
        rgb.set_rgb((255, 0, 0))    # Mode 0 → Red
    elif layer == 1:
        rgb.set_rgb((0, 255, 0))    # Mode 1 → Green
    elif layer == 2:
        rgb.set_rgb((0, 0, 255))    # Mode 2 → Blue

keyboard.after_layer_change = after_layer_change


# KEYMAP (3x4)

keyboard.keymap = [

    #          MODE 0 
    [
        KC.Q, KC.W, KC.E,
        KC.A, KC.S, KC.D,
        KC.Z, KC.X, KC.C,
        KC.TO(1), KC.NO, KC.NO,
    ],

    #          MODE 1 
    [
        KC.ONE, KC.TWO, KC.THREE,
        KC.FOUR, KC.FIVE, KC.SIX,
        KC.SEVEN, KC.EIGHT, KC.NINE,
        KC.TO(2), KC.NO, KC.NO,
    ],

    #        MODE 2 
    [
        KC.F1, KC.F2, KC.F3,
        KC.F4, KC.F5, KC.F6,
        KC.F7, KC.F8, KC.F9,
        KC.TO(0), KC.NO, KC.NO,
    ],
]


if __name__ == "__main__":
    after_layer_change(0)  
    keyboard.go()
