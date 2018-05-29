# Materializer
Python script to make a pictures "materialize" out of a stream of bits in the terminal

## What is it?
1. `image_to_ascii.py`: Python script to downsample and binarize an image
    to an ASCII image using thresholding.
1. `materialize.py`: Python script using curses to show a stream of bits
    (running from top to bottom) in which an ASCII image slowly
    materializes.
1. `Images`: some sample images.
1. `AsciiImages`: some sample ASCII images.

## How to use it?
To convert an image file (e.g., PNG) to an ASCII image:
```bash
$ ./image_to_ascii.py Images/bug.png > bug.txt
```
To get help on command line options to fine-tune:
```bash
$ ./image_to_ascii.py --help
```

To show a bit stream in the terminal out of which an ASCII image
materializes:
```bash
$ ./materialize.py AsciiImages/bug.txt
```
To get help on command line options to fine-tune:
```bash
$ ./materialize.py --help
```
