#!/usr/bin/env python3

import os
import sys
import argparse
from PIL import Image
import glob

# Thanks to https://stackoverflow.com/a/54547257
def dir_path(file_path):
    if os.path.isfile(file_path):
        return file_path
    else:
        raise argparse.ArgumentTypeError(f'Supplied argument "{file_path}" is not a valid file path.')


parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(
    description='A script to convert pre-generated apriltag .png files into SVG format.',
    epilog='Example: "python tag_to_svg.py gen_apriltags --tag_family tag36h11 --tag_ids 3-10 --size=20mm"'
)

parser.add_argument(
    '--out_dir', type=str, dest="out_dir",
    help='The path to the SVG output file.'
)
parser.add_argument(
    '--size', type=str, required=False, default='20mm', dest="svg_size", 
    help='The size (edge length) of the generated svg such as "20mm" "2in" "20px"'
)
parser.add_argument(
    '--tag_family', type=str, required=False, default='tag36h11', dest="tag_family", 
    help='Tag family same like dir name"'
)
parser.add_argument(
    '--tag_ids', type=str, required=False, default='0-10', dest="tag_ids", 
    help='All wanted tag ids of the given family, from-to, like "0-10 or "0-0" for only tag with id zero"'
)

parser.add_argument(
    '--suffix', type=str, required=False, default='gen', dest="suffix", 
    help='Suffix of the output images, example: 110 as size of AprilTag in mmm'
)


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

def create_dir_if_not_exists(dir_path):
    print(dir_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def main():
    args = parser.parse_args()
    out_dir = args.out_dir + '/'
    svg_size = args.svg_size
    tag_familie = args.tag_family
    tag_ids = args.tag_ids

    tag_start = int(tag_ids.split('-')[0])  
    tag_end = int(tag_ids.split('-')[1])
    print(out_dir)
    create_dir_if_not_exists(out_dir+'/')


    for tag_file in sorted(glob.glob(f"{tag_familie}/tag*"))[tag_start:tag_end+1]:
        apriltag_svg = None
        with Image.open(tag_file, 'r') as im:

            width, height = im.size
            pix_vals = im.load()

            apriltag_svg = gen_apriltag_svg(width, height, pix_vals, svg_size)

        assert apriltag_svg is not None, 'Error: Failed to create SVG.'

        out_file = f"{out_dir}{tag_file.split('.')[0].split('/')[1]}_{args.suffix}.svg"

        with open(out_file, 'w') as fp:
            fp.write(apriltag_svg)

        print(f'Output SVG file: {out_file} with size: {svg_size}')

if __name__ == "__main__":
    main()
