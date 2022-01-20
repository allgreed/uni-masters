#!/usr/bin/env python
from PIL import Image, ImageColor

COLOR_MAP = {
    1: ImageColor.getrgb("#F9B3D1"),
    2: ImageColor.getrgb("#00FF00"),
    3: ImageColor.getrgb("#000000"),
    4: ImageColor.getrgb("#2A0800"),
    5: ImageColor.getrgb("#FFFFFF"),
    0: ImageColor.getrgb("#775144"),
}
N = 1000
M = 6


def main():
    im = Image.new('RGB', (2 * (N + 1) ,N))

    r = [1]
    for i in range(N):
        r = next_row(r, lambda x: x % M)
        draw_row(im, r, i)

    im.save('ble.png') # or any image format
    print("fin!")


def draw_row(image, row, y):
    x_offset = (image.width - len(row) * 2) // 2
    for i, value in enumerate(row):
        image.putpixel((2 * i + x_offset, y), COLOR_MAP[value])
        image.putpixel((2 * i + 1 + x_offset, y), COLOR_MAP[value])


def next_row(row, f):
    new_row = []
    for i in range(len(row) + 1):
        new_row.append(f(get_or_default(row, i - 1, 0) + get_or_default(row, i, 0)))
    return new_row


def get_or_default(arr, idx, default):
    if idx < 0:
        return default

    try:
        return arr[idx]
    except IndexError:
        return default


assert len(COLOR_MAP) >= M, "prawdaż, istnieje tyle kolorów coby pokolorować modulo była możliwość"

if __name__ == "__main__":
    main()
