import logging
import random
import uuid
from collections import Counter
from pathlib import Path
from functools import cache

import arcade
from PIL import Image

from space_collector.game.constants import MAP_DIMENSION
from space_collector.viewer.constants import (
    MAP_MIN_X,
    MAP_MAX_X,
    MAP_MIN_Y,
    MAP_MAX_Y,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

MAP_WIDTH = MAP_MAX_X - MAP_MIN_X
MAP_HEIGHT = MAP_MAX_Y - MAP_MIN_Y


def map_value_to_window(value: float) -> float:
    return max(
        int(value / MAP_DIMENSION * MAP_WIDTH),
        int(value / MAP_DIMENSION * MAP_HEIGHT),
    )


def map_coord_to_window_coord(x: float, y: float) -> tuple[int, int]:
    return (
        int(x / MAP_DIMENSION * MAP_WIDTH) + MAP_MIN_X,
        int(y / MAP_DIMENSION * MAP_HEIGHT) + MAP_MIN_Y,
    )


def find_image_files(directory: Path | str) -> list[Path]:
    if isinstance(directory, str):
        directory = Path(directory)
    return [
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix in (".jpg", ".png", ".jpeg")
    ]


def random_sprite(path: str) -> arcade.Sprite:
    sprite_image = random.choice(find_image_files(path))
    sprite = arcade.Sprite(sprite_image)
    sprite.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    sprite.width = SCREEN_WIDTH
    sprite.height = SCREEN_HEIGHT
    return sprite


@cache
def hue(image_path: str) -> int:
    """Get most common hue in important pixels (saturated, not transparent…)

    Args:
        image_path: path of the image to analyze

    Returns:
        the most common hue (rounded to tens)
    """
    image = Image.open(image_path)
    alphas = image.getdata(band=3)
    hsv_image = image.convert("HSV")
    hues = hsv_image.getdata(band=0)
    saturations = hsv_image.getdata(band=1)
    values = hsv_image.getdata(band=2)
    important_hues = [
        hue // 10 * 10
        for hue, saturation, value, alpha in zip(hues, saturations, values, alphas)
        if saturation > 50 and value > 50 and alpha != 0
    ]
    counter = Counter(important_hues)
    return counter.most_common(1)[0][0]


@cache
def hue_changed_texture(image_path: str, target_hue: int) -> arcade.Texture:
    logging.info("Managing %s", image_path)
    original_image = Image.open(image_path)
    original_hue = hue(image_path)
    offset_hue = 256 + target_hue - original_hue
    alpha_channel = original_image.split()[-1]
    hsv_image = original_image.convert("HSV")
    h, s, v = hsv_image.split()
    hue_data = h.point(lambda i: (i + offset_hue) % 256)
    adjusted_hue_image = Image.merge("HSV", (hue_data, s, v))
    adjusted_hue_image_rgb = adjusted_hue_image.convert("RGB")
    final_image = Image.merge("RGBA", (*adjusted_hue_image_rgb.split(), alpha_channel))
    return arcade.Texture(name=str(uuid.uuid4()), image=final_image)
