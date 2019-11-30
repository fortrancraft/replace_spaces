#!/usr/bin/env python3


# Find and replace spaces with a new string in all results from a search.

import argparse
import glob
import os

import replace_spaces as rs

parser = argparse.ArgumentParser()

parser.add_argument('search', help='input the search-string to use ' + \
                    'for finding files and directories to process.')

parser.add_argument('--rstr', default='_', help='set the character ' + \
                    'or string to replace spaces with')

parser.add_argument('--squash', default=False, action='store_true',
                    help='Squash multiple spaces into one space prior ' + \
                    'to renaming.')

parser.add_argument('-i, ', '--interactive', default=False,
                    action='store_true', help='Execute the function ' + \
                    'interactively')

parser.add_argument('-w', '--walk', default=False, action='store_true',
                    help='Walk through all directories found with the ' + \
                    'search string')

parser.add_argument('--verbose', '-v', action='count', default=0,
                    help='set the output printing verbosity level')

parser.add_argument('--dry-run', action='store_true', default=False,
                    help='execute the script without moving the ' + \
                    'input file/dir')

args = parser.parse_args()

if args.verbose > 1:
    print(' ')
    print('replace_spaces_batch :')
    print(' ')
    print('args.search      = {}'.format(args.search))
    print('args.rstr        = {}'.format(args.rstr))
    print('args.squash      = {}'.format(args.squash))
    print('args.interactive = {}'.format(args.interactive))
    print('args.walk        = {}'.format(args.walk))
    print('args.verbose     = {}'.format(args.verbose))
    print('args.dry_run     = {}'.format(args.dry_run))

verbose_nested = max(0, args.verbose-1)

glob_items = glob.glob(args.search)

if args.verbose > 1:
    print('glob_items = {}'.format(glob_items))

for glob_item in glob_items:

    if args.verbose > 1:
        print(' ')
        print('glob_item = {}'.format(glob_item))
        print('is file?  = {}'.format(os.path.isfile(glob_item)))
        print('is dir?   = {}'.format(os.path.isdir(glob_item)))

    if args.walk or True:

        # Walk through any found directories, and process every file.
        for dir_name, sub_dir_list, file_list in os.walk(glob_item):
            if args.verbose > 1:
                print(' ')
                print('dir_name     = {}'.format(dir_name))
                print('sub_dir_list = {}'.format(sub_dir_list))
            if args.verbose > 1:
                print('file_list    = {}'.format(file_list))

            for file in file_list:
                file_path = os.path.join(dir_name, file)

                if args.verbose > 0:
                    print(' ')
                    print('processing file : {}'.format(file_path))

                rs.replace_spaces(file_path,
                                  rstr=args.rstr,
                                  squash=args.squash,
                                  interactive=args.interactive,
                                  dry_run=args.dry_run,
                                  verbose=verbose_nested)

    else:

        rs.replace_spaces(glob_item,
                          rstr=args.rstr,
                          squash=args.squash,
                          interactive=args.interactive,
                          dry_run=args.dry_run,
                          verbose=verbose_nested)
