#!/usr/bin/env python

from argparse import ArgumentParser
import curses
import random
import sys
import time

def new_line(cols, prob=0.5):
    population = ['0', '1']
    weights = [1.0 - prob, prob]
    return random.choices(population, weights=weights, k=cols)

def new_screen(screen, lines, cols, prob=0.5):
     screen.insert(0, new_line(cols, prob))
     if len(screen) > lines:
         _ = screen.pop()
    
    
def main(stdscr, options):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
    figure_char = ' '
    stdscr.clear()
    stdscr.refresh()
    screen = []
    pict = read_picture(options.picture)
    lines = len(pict)
    if lines == 0 or lines >= curses.LINES:
        print('### error: picture lines {lines} is invalid',
              file=sys.stdeer)
        sys.exit(1)
    cols = len(pict[0])
    if cols == 0 or cols >= curses.COLS:
        print('### error: picture columns {cols} is invalid',
              file=sys.stdeer)
        sys.exit(1)
    stdscr.border(' ')
    for line_nr in range(lines):
        for col_nr in range(cols):
            stdscr.addstr(line_nr, col_nr, ' ', curses.color_pair(1))
    stdscr.refresh()
    if options.verbose:
        print(f'{lines} x {cols}', file=sys.stderr)
    while True:
        new_screen(screen, lines, cols, options.prob)
        if options.verbose:
            print(f'{len(screen)} x {len(screen[0])}', file=sys.stderr)
        line_nr = 0
        for line in screen:
            col_nr = 0
            for char in line:
                if pict[line_nr][col_nr] == '2':
                    stdscr.addstr(line_nr, col_nr, figure_char,
                                  curses.color_pair(2))
                else:
                    if pict[line_nr][col_nr] == '1':
                        if random.random() < options.appear_prob:
                            pict[line_nr][col_nr] = '2'
                    stdscr.addstr(line_nr, col_nr, char,
                                  curses.color_pair(1))
                col_nr += 1
            line_nr += 1
        stdscr.refresh()
        time.sleep(options.sleep)


def read_picture(file_name):
    pict = []
    with open(file_name, 'r') as pict_file:
        for line in pict_file:
            pict.append(list(line.strip()))
    return pict
    

if __name__ == '__main__':
    arg_parser = ArgumentParser(description='matrix-like screen animation')
    arg_parser.add_argument('picture', help='picture to show')
    arg_parser.add_argument('--sleep', type=float, default=0.2,
                            help='time to sleep between screen refresh')
    arg_parser.add_argument('--prob', type=float, default=0.5,
                            help='probability for showing 1')
    arg_parser.add_argument('--appear-prob', type=float, default=0.1,
                            help='probability for showing 1')
    arg_parser.add_argument('--verbose', action='store_true',
                            help='verbose output for debugging')
    options = arg_parser.parse_args()
    try:
        curses.wrapper(main, options)
    except KeyboardInterrupt:
        pass
