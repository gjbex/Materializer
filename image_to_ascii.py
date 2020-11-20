#!/usr/bin/env python

from argparse import ArgumentParser
import numpy as np
import skimage
import skimage.io

def image_to_ascii(image, lines, cols, threshold):
    img_data = skimage.io.imread(image)
    pixel_data = img_data.mean(axis=2) if img_data.ndim == 3 else img_data
    ascii = np.empty((lines, cols), dtype=np.int)
    height = pixel_data.shape[0]//lines
    width = pixel_data.shape[1]//cols
    for line_nr in range(lines):
        for col_nr in range(cols):
            pixel = pixel_data[line_nr*height:(line_nr + 1)*height,
                               col_nr*width:(col_nr + 1)*width].mean()/256.0
            ascii[line_nr, col_nr] = 1 if pixel < threshold else 0
    return ascii

def write_image(image):
    for line_nr in range(image.shape[0]):
        for col_nr in range(image.shape[1]):
            print(image[line_nr, col_nr], end='')
        print()

if __name__ == '__main__':
    arg_parser = ArgumentParser(description='convert image to ascii')
    arg_parser.add_argument('image', help='image file to process')
    arg_parser.add_argument('--lines', type=int, default=23,
                            help='number of ascii lines')
    arg_parser.add_argument('--cols', type=int, default=79,
                            help='number of ascii columns')
    arg_parser.add_argument('--threshold', type=float, default=0.7,
                            help=('threshold above which pixel is '
                                  'considered as white'))
    options = arg_parser.parse_args()
    ascii = image_to_ascii(options.image, options.lines, options.cols,
                           options.threshold)
    write_image(ascii)
