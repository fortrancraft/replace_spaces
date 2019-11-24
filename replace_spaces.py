#!/usr/bin/env python3

__author__      = 'Jeffrey R. Bell'
__license__     = "GPL-3.0"
__version__     = "0.0.0"
__status__      = "beta"
__description__ = 'This command line utility will replace spaces ' + \
    'in a file or directory name with a string.'
__email__       = 'fortrancraft@gmail.com',
__url__         = 'https://github.com/fortrancraft/replace_spaces.py',


import argparse
import datetime
import gzip
import os
import shutil


def make_arg_parser():
    """Make an argument parser."""
    parser = argparse.ArgumentParser()

    parser.add_argument('input_name',
        help='input the file or directory to replace spaces in')

    parser.add_argument('--char', default='_',
        help='set the character or string to replace spaces with')

    parser.add_argument('--squash', default=False, action='store_true',
        help='Squash multiple spaces into one space prior to renaming.')

    parser.add_argument('--verbose', '-v', action='count', default=0,
        help='set the output printing verbosity level')

    parser.add_argument('--dry-run', action='store_true', default=False,
        help='execute the script without moving the input file/dir')

    args = parser.parse_args()

    if args.verbose > 1:
        print('args.input_name = {}'.format(args.input_name))
        print('args.char       = {}'.format(args.char))
        print('args.squash     = {}'.format(args.squash))
        print('args.verbose    = {}'.format(args.verbose))
        print('args.dry_run    = {}'.format(args.dry_run))

    return args


def is_file_or_dir(item, raise_exception=False):
    """Test if an input item is a file or directory.

    Parameters
    ----------
    item : str
        file or directory path string
    raise_exception : Bool
        if True, then an exception is raised stating the file/dir doesn't exist

    Returns
    -------
    Bool : True if item is a file or directory
    """
    q = os.path.isfile(item) or \
        os.path.isdir(item)

    if raise_exception and not q:
        msg = 'Input file/directory, "{}" does not exist!'\
            .format(item)
        raise FileNotFoundError(msg)

    return q


def main():
    """Squash (remove and replace) spaces in an input file/dir.
    """

    # Prepare for execution.
    args = make_arg_parser()
    if args.dry_run:
        drnote = ' (dry-run)'
    else:
        drnote = ''

    # Make sure the input is a file or dir exists.
    exists = False
    if is_file_or_dir(args.input_name, raise_exception=True):
        exists = True

    # Split the input_item name into a path, name and extension (if exists).
    item_dir = os.path.dirname(args.input_name)
    basename = os.path.basename(args.input_name)
    item_name, item_ext = os.path.splitext(basename)

    # Squash spaces if requested.
    if args.squash:
        # Recursively replace two spaces with one until no changes occur.
        old_item_name = '{}'.format(item_name)
        done = False
        iter = 0
        while not done:
            iter += 1
            new_item_name = old_item_name.replace('  ', ' ')

            if args.verbose > 0:
                print(' ')
                print('iter = {}'.format(iter))
                print('old_item_name = "{}"'.format(old_item_name))
                print('new_item_name = "{}"'.format(new_item_name))

            if new_item_name == old_item_name:
                done = True
                item_name = '{}'.format(new_item_name)
            else:
                old_item_name = '{}'.format(new_item_name)

            # Quit if squashing is not working within a reasonable iteration.
            if iter > 10000:
                msg = 'Failed to squash spaces in the input file/dir name!'
                raise ValueError(msg)

    # Replace all spaces in the item name with the input character.
    new_name = item_name.replace(' ', args.char)
    new_path = os.path.join(item_dir, new_name + item_ext)

    if args.verbose > 0:
        print(' ')
        print('item_dir    = {}'.format(item_dir))
        print('basename    = {}'.format(basename))
        print('item_name   = {}'.format(item_name))
        print('item_ext    = {}'.format(item_ext))
        print(' ')
        print('new_name = {}'.format(new_name))
        print('new_path = {}'.format(new_path))

    # Rename the item.
    if not args.dry_run:
        # Check if the input item name is the same as the new (i.e. unchanged).
        if item_name == new_name:
            print('\n--> New file/dir name matches input name! Exiting...')
            return

        # Check if the file/dir exists already to prevent over writing.
        if is_file_or_dir(new_path):
            msg = 'new_path = {} alreadys exists!'.format(new_path)
            raise FileExistsError(msg)
        else:
            # Move the item in place to the new name and path.
            shutil.move(args.input_name, new_path)

    # Check if the item move was successful.
    if args.dry_run:
        pass
    else:

        # Check if the item move worked.
        if not is_file_or_dir(new_path):
            msg = 'Failed to rename the file/dir!'
            raise FileNotFoundError(msg)

    out_fmt = 'moved {} to {}{}'
    print(out_fmt.format(args.input_name, new_path, drnote))

if __name__ == "__main__":
    main()
