#!/usr/bin/env python3

__author__ = 'Jeffrey R. Bell'
__license__ = "GPL-3.0"
__version__ = "0.0.1"
__status__ = "beta"
__description__ = 'This command line utility will replace spaces ' + \
    'in a file or directory name with a string.'
__email__ = 'fortrancraft@gmail.com',
__url__ = 'https://github.com/fortrancraft/replace_spaces.py',


import argparse
import os
import shutil


def make_arg_parser():
    """Make an argument parser."""
    parser = argparse.ArgumentParser()

    parser.add_argument('input_name', help='input the file or directory ' + \
                        'to replace spaces in')

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

    if args.verbose > 1:
        print('args.input_name  = {}'.format(args.input_name))
        print('args.rstr        = {}'.format(args.rstr))
        print('args.squash      = {}'.format(args.squash))
        print('args.interactive = {}'.format(args.interactive))
        print('args.verbose     = {}'.format(args.verbose))
        print('args.dry_run     = {}'.format(args.dry_run))

    return args


def is_file_or_dir(item):
    """Test if an input item is a file or directory.

    Parameters
    ----------
    item : str
        file or directory path string

    Returns
    -------
    Bool : True if item is a file or directory
    """
    q = os.path.isfile(item) or \
        os.path.isdir(item)

    return q


def ask_rename(input_name, new_path):
    """Ask to rename/move the item.

    Parameters
    ----------
    input_name : str
        input item to rename
    new_path : str
        new path of the input item

    Returns
    -------
    answer : Bool
        True if the input answer is
    """
    if input_name == new_path:
        # Don't ask to rename, but state the output is the same as the input.
        print(' ')
        print('input_name : {}'.format(input_name))
        print('new_path   : {}'.format(new_path))
        print('    --> Output name is the same as the input!')
        answer = False
    else:
        print(' ')
        print('Replace \n    {}\nwith\n    {}\n?'\
            .format(input_name, new_path))
        input_rename_item = input('[yes]/no : ')
        if input_rename_item.lower() in ['yes', 'y', 'ye', '']:
            answer = True
        else:
            answer = False
    return answer


def replace_spaces(input_name, rstr='-', squash=True, interactive=False,
                   dry_run=False, verbose=0):
    """Replace spaces in an input file/dir with a new string.

    Parameters
    ----------
    input_name : str
        file or directory path to replace spaces in
    rstr : str
        replacement string
    squash : bool
        True to squash multiple spaces into one prior to replacing
    interactive : bool
        Prompt before modifying the input item
    verbose : int
        printing verbosity level
    """

    # Prepare a dry-run note to use with printing.
    if dry_run:
        drnote = ' (dry-run)'
    else:
        drnote = ''

    # Make sure the input is a file or dir exists.
    exists = False
    if is_file_or_dir(input_name):
        exists = True
    else:
        # Return since there is nothing to do.
        print(' ')
        print('--> The input file/dir does not exist! Nothing to do...')
        return

    # Split the input_item name into a path, name and extension (if exists).
    item_dir = os.path.dirname(input_name)
    basename = os.path.basename(input_name)
    item_name, item_ext = os.path.splitext(basename)

    # Squash spaces if requested.
    if squash:
        # Recursively replace two spaces with one until no changes occur.
        old_item_name = '{}'.format(item_name)
        done = False
        iter = 0
        while not done:
            iter += 1
            new_item_name = old_item_name.replace('  ', ' ')

            if verbose > 0:
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
    new_name = item_name.replace(' ', rstr)
    new_path = os.path.join(item_dir, new_name + item_ext)

    if verbose > 0:
        print(' ')
        print('item_dir    = {}'.format(item_dir))
        print('basename    = {}'.format(basename))
        print('item_name   = {}'.format(item_name))
        print('item_ext    = {}'.format(item_ext))
        print(' ')
        print('new_name = {}'.format(new_name))
        print('new_path = {}'.format(new_path))

    # Initialize the replace item prompt action.
    rename_item = True

    # Rename the item.
    if not dry_run:
        # Check if the input item name is the same as the new (i.e. unchanged).
        if item_name == new_name:
            print(' ')
            print('item_name : {}'.format(item_name))
            print('new_name  : {}'.format(new_name))
            print('--> New file/dir name matches input name!')
            return

        # Check if the file/dir exists already to prevent over writing.
        if is_file_or_dir(new_path):
            # Return since there is nothing to do.
            print(' ')
            print('--> The new file/dir path already exists! Nothing to do...')
            return

        else:
            # Move the item in place to the new name and path.
            if interactive:
                rename_item = ask_rename(input_name, new_path)

            if rename_item:
                shutil.move(input_name, new_path)

    # Check if the item move was successful.
    if dry_run:
        # If interactively running, ask to rename. Otherwise pass.
        if interactive:
            rename_item = ask_rename(input_name, new_path)

    else:

        # Check if the item move worked.
        if rename_item:
            if not is_file_or_dir(new_path):
                msg = 'Failed to rename the file/dir!'
                raise FileNotFoundError(msg)

    if rename_item:
        out_fmt = 'moved {} to {}{}'
        print(out_fmt.format(input_name, new_path, drnote))


def main():
    """Squash (remove and replace) spaces in an input file/dir.
    """

    # Fetch command line arguments.
    args = make_arg_parser()

    # Execute the replace_spaces function with the requested options.
    replace_spaces(args.input_name, rstr=args.rstr, squash=args.squash,
                   interactive=args.interactive, dry_run=args.dry_run,
                   verbose=args.verbose)

if __name__ == "__main__":
    main()
