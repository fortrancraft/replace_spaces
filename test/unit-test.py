#!/usr/bin/env python3

import argparse
import glob
import os


parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', action='count', default=0,
    help='set the output printing verbosity level (this script only)')
args = parser.parse_args()


script='../replace_spaces.py'

idx = 0
for arg_squash in ['', '--squash']:

    for arg_rstr in ['--rstr=-', '--rstr=__']:

        for arg_verbose in ['', '-v', '-vv']:

            # Create a copy of the examples directory and use the copy for
            # testing this permutation.
            idx += 1
            dir_work = 'test-examples-{:>02d}'.format(idx)
            os.system('rm -rf ' + dir_work)
            os.system('cp -r examples ' + dir_work)
            test_items = glob.glob(dir_work + '/*')

            for arg_dry_run in ['--dry-run', '']:

                for test_item in test_items:


                    cmd = script + ' "' + test_item + '"' + \
                        ' ' + arg_squash + \
                        ' ' + arg_rstr + \
                        ' ' + arg_verbose + \
                        ' ' + arg_dry_run

                    if args.verbose > 0:
                        print('\n' + '#'*70)
                        print('##')
                        print(' ')
                        print('test_item = "{}"'.format(test_item))
                        print('cmd = {}'.format(cmd))

                    os.system(cmd)

                    if args.verbose > 0:
                        print(' ')
                        print('##')
                        print('#'*70)
