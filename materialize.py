#!/usr/bin/env python

from argparse import ArgumentParser
import curses
import random
import sys
import time

def new_line(cols, started_cols, prob=0.5):
    population = ['0', '1']
    weights = [1.0 - prob, prob]
    line = random.choices(population, weights=weights, k=cols)
    for col_nr, started in enumerate(started_cols):
        if not started:
            line[col_nr] = ' '
    return line

def new_screen(screen, lines, cols, started_cols, prob=0.5):
     screen.insert(0, new_line(cols, started_cols, prob))
     if len(screen) > lines:
         _ = screen.pop()
    
def update_started_cols(started_cols, prob):
    for col_nr in range(len(started_cols)):
        if random.random() < prob:
            started_cols[col_nr] = started_cols[col_nr] or True
    
def main(stdscr, options):
    if options.bg_color == 'white':
        bg_color = curses.COLOR_WHITE
    else:
        bg_color = curses.COLOR_BLACK
    curses.init_pair(1, curses.COLOR_GREEN, bg_color)
    curses.init_pair(2, curses.COLOR_RED, bg_color)
    figure_char = '0'
    stdscr.clear()
    stdscr.refresh()
    screen = []
    pict = read_picture(options.picture)
    lines = len(pict)
    if lines == 0 or lines >= curses.LINES:
        curses.endwin()
        print(f'### error: picture lines {lines} is invalid, enlarge your terminal',
              file=sys.stderr)
        sys.exit(1)
    cols = len(pict[0])
    if cols == 0 or cols >= curses.COLS:
        curses.endwin()
        print(f'### error: picture columns {cols} is invalid, enlarge your terminal',
              file=sys.stderr)
        sys.exit(1)
    stdscr.border(' ')
    for line_nr in range(lines):
        for col_nr in range(cols):
            stdscr.addstr(line_nr, col_nr, ' ', curses.color_pair(1))
    stdscr.refresh()
    started_cols = random.choices([True, False],
                                  weights=[options.ragged_prob,
                                           1.0 - options.ragged_prob],
                                  k=cols)
    while True:
        new_screen(screen, lines, cols, started_cols, options.one_prob)
        if options.verbose:
            print(f'{len(screen)} x {len(screen[0])}', file=sys.stderr)
        line_nr = 0
        for line in screen:
            col_nr = 0
            for char in line:
                if pict[line_nr][col_nr] == '2':
                    stdscr.addstr(line_nr, col_nr, figure_char,
                                  curses.color_pair(2) | curses.A_BOLD)
                else:
                    if pict[line_nr][col_nr] == '1':
                        if (random.random() < options.appear_prob and
                                started_cols[col_nr]):
                            pict[line_nr][col_nr] = '2'
                    stdscr.addstr(line_nr, col_nr, char,
                                  curses.color_pair(1))
                col_nr += 1
            line_nr += 1
        stdscr.refresh()
        time.sleep(options.sleep)
        update_started_cols(started_cols, options.ragged_prob)

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
    arg_parser.add_argument('--one-prob', type=float, default=0.5,
                            help='probability for showing 1')
    arg_parser.add_argument('--appear-prob', type=float, default=0.1,
                            help='probability for showing 1')
    arg_parser.add_argument('--ragged-prob', type=float, default=0.1,
                            help='probability for starting a column')
    arg_parser.add_argument('--bg-color', choices=['black', 'white'],
                            default='black', help='background color')
    arg_parser.add_argument('--verbose', action='store_true',
                            help='verbose output for debugging')
    options = arg_parser.parse_args()
    try:
        curses.wrapper(main, options)
    except KeyboardInterrupt:
        pass
