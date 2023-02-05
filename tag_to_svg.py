#!/usr/bin/env python3

import os
import sys
import argparse
from PIL import Image

# Thanks to https://stackoverflow.com/a/54547257
def dir_path(file_path):
    if os.path.isfile(file_path):
        return file_path
    else:
        raise argparse.ArgumentTypeError(f'Supplied argument "{file_path}" is not a valid file path.')


parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(
    description='A script to convert pre-generated apriltag .png files into SVG format.',
    epilog='Example: "python tag_to_svg.py tagStandard52h13/tag52_13_00007.png tag52_13_00007.svg --size=20mm"'
)
parser.add_argument(
    'tag_file', type=dir_path, 
    help='The path to the apriltag png you want to convert.'
)
parser.add_argument(
    'out_file', type=str, 
    help='The path to the SVG output file.'
)
parser.add_argument(
    '--size', type=str, required=False, default='20mm', dest="svg_size", 
    help='The size (edge length) of the generated svg such as "20mm" "2in" "20px"'
)
# TODO add support for a blank margin around the tag
# parser.add_argument(
#     '--margin', type=int, required=False, default='0', dest="tag_margin", 
#     help='The size (in grid squares) of the white margin around the apriltag'
# )


def gen_apriltag_svg(width, height, pixel_array, size):
    def gen_rgba(rbga):
        (_r, _g, _b, _raw_a) = rbga
        _a = _raw_a / 255
        return f'rgba({_r}, {_g}, {_b}, {_a})'

    def gen_gridsquare(row_num, col_num, pixel):
        _rgba = gen_rgba(pixel)
        _id = f'box{row_num}-{col_num}'
        return f'\t<rect width="1" height="1" x="{row_num}" y="{col_num}" fill="{_rgba}" id="{_id}"/>\n'

    svg_text = '<?xml version="1.0" standalone="yes"?>\n'
    svg_text += f'<svg width="{size}" height="{size}" viewBox="0,0,{width},{height}" xmlns="http://www.w3.org/2000/svg">\n'
    for _y in range(height):
        for _x in range(width):
            svg_text += gen_gridsquare(_x, _y, pixel_array[_x, _y])
    svg_text += '</svg>\n'

    return svg_text

def main():
    args = parser.parse_args()
    tag_file = args.tag_file
    out_file = args.out_file
    svg_size = args.svg_size
    # tag_margin = args.tag_margin #TODO no support for margin yet

    apriltag_svg = None

    with Image.open(tag_file, 'r') as im:

        width, height = im.size
        pix_vals = im.load()
        
        apriltag_svg = gen_apriltag_svg(width, height, pix_vals, svg_size)

    assert apriltag_svg is not None, 'Error: Failed to create SVG.'

    with open(out_file, 'w') as fp:
        fp.write(apriltag_svg)

    print(f'Output SVG file: {out_file} with size: {svg_size}')

if __name__ == "__main__":
    main()
