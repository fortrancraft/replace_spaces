#!/usr/bin/env python3


# Replace spaces with dashes in all of the files and directories in the
# current path.

import argparse
import glob
import os

import replace_spaces as rs

print('dir(rs) = {}'.format(dir(rs)))
parser = argparse.ArgumentParser()

parser.add_argument('--search', help='input the search-string to use ' + \
                    'for finding files and directories to process.')

parser.add_argument('--rstr', default='_', help='set the character ' + \
                    'or string to replace spaces with')

parser.add_argument('--squash', default=False, action='store_true',
                    help='Squash multiple spaces into one space prior ' + \
                    'to renaming.')

parser.add_argument('-i, ', '--interactive', default=False,
                    action='store_true', help='Execute the function ' + \
                    'interactively')

parser.add_argument('--verbose', '-v', action='count', default=0,
                    help='set the output printing verbosity level')

parser.add_argument('--dry-run', action='store_true', default=False,
                    help='execute the script without moving the ' + \
                    'input file/dir')

args = parser.parse_args()


print(' ')
print('args.search  = {}'.format(args.search))
print(' ')

items = glob.glob(args.search)
for item in items:
    print('item = {}'.format(item))

    rs.replace_spaces(item, rstr=args.rstr, squash=args.squash,
                      interactive=args.interactive, dry_run=args.dry_run,
                      verbose=args.verbose)
