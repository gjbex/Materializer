# Materializer

This is a collection of tools to create techie visuals for communication
purposes, e.g., on social media.

Materializer is a scripts to make a pictures "materialize" out of a 
stream of bits in the terminal (cfr. "The Matrix").

Word clouds can be made using a Jupyter notebook.


## What is it?
1. Materializer
    1. `image_to_ascii.py`: Python script to downsample and binarize an image
        to an ASCII image using thresholding.
    1. `materialize.py`: Python script using curses to show a stream of bits
        (running from top to bottom) in which an ASCII image slowly
        materializes.
    1. `Images`: some sample images.
    1. `AsciiImages`: some sample ASCII images.
1. `Word clouds
    1. wordcloud.ipynb`: Jupyter notebook to create word clouds.

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

You may want to use a retro terminal for more impressive effects.


## Requirements

  * Python 3.6+
  * scikit-image
  * numpy
  * jupyter lab
  * wordcloud
