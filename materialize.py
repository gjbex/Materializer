#!/usr/bin/env python

from argparse import ArgumentParser
import curses
import random
import sys
import time

COLORS = {
    'black':   curses.COLOR_BLACK,
    'white':   curses.COLOR_WHITE,
    'red':     curses.COLOR_RED,
    'green':   curses.COLOR_GREEN,
    'blue':    curses.COLOR_BLUE,
    'magenta': curses.COLOR_MAGENTA,
    'yellow':  curses.COLOR_YELLOW,
    'cyan':    curses.COLOR_CYAN,
}

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
    bg_color = COLORS[options.bg_color]
    curses.init_pair(1, COLORS[options.fg_color1], bg_color)
    curses.init_pair(2, COLORS[options.fg_color2], bg_color)
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
        for line_nr, line in enumerate(screen):
            for col_nr, char in enumerate(line):
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
        stdscr.refresh()
        time.sleep(options.sleep)
        update_started_cols(started_cols, options.ragged_prob)

def read_picture(file_name):
    pict = []
    with open(file_name, 'r') as pict_file:
        pict.extend(list(line.strip()) for line in pict_file)
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
    arg_parser.add_argument('--bg-color', choices=COLORS.keys(),
                            default='black', help='background color')
    arg_parser.add_argument('--fg-color1', choices=COLORS.keys(),
                            default='green', help='first foreground color')
    arg_parser.add_argument('--fg-color2', choices=COLORS.keys(),
                            default='red', help='second foreground color')
    arg_parser.add_argument('--verbose', action='store_true',
                            help='verbose output for debugging')
    options = arg_parser.parse_args()
    try:
        curses.wrapper(main, options)
    except KeyboardInterrupt:
        pass
