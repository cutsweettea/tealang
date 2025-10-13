import argparse
import logging
import os
import sys

from interpreter import Teaterpreter

from tokenizing.keywords import *
from tokenizing.operators import *

def runasfastaspossiblebutitspythonsoitsokifitsalittleslow():
    # create argument parser
    argp = argparse.ArgumentParser(
        description='tea interpreter',
        epilog='i love tea'
    )

    # create basic arguments
    argp.add_argument('file_name', type=str, help='path to tea file')

    # create logging argument group
    logging_group = argp.add_argument_group(title='logging', description='arguments related to information printed')
    logging_group.add_argument('-ll', '--log-level', type=int, help='the minimum log level to use', choices=[logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR, logging.CRITICAL], default=logging.CRITICAL, dest='log_level')

    # mode arguments (what to do)
    mode_group = argp.add_argument_group(title='modes', description='modes for the program to work in')
    mode_group.add_argument('-c', '--compile', action='store_true', help='whether to compile the given script', dest='compile')

    # compilation argument group
    compilation_group = argp.add_argument_group(title='compilation', description='arguments related to compiling a script')
    compilation_group.add_argument('-co', '--compile-output', type=str, help='path to output for compilation', dest='compile_output')
    compilation_group.add_argument('-s', '--skip-file-exist', action='store_true', help='whether to skip the file already exists dialogue', dest='skip_fae')

    # running arguments

    args = argp.parse_args()

    # setup logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(encoding='utf-8', level=args.log_level, format='[%(asctime)s] [%(filename)s:%(lineno)s:%(name)s] [%(levelname)s] %(message)s', datefmt='%s')

    # setup the tea
    tea_interp = Teaterpreter(args.file_name)

    if args.compile:
        if args.compile_output == None:
            print(f'-co / --compile-output must be set when compiling')
            sys.exit(1)

        if not args.skip_fae:
            if os.path.exists(args.compile_output):
                try:
                    theverylargevariablenamerepresentingayesorno = input(f'file "{args.compile_output}" already exists? replace (y/n): ').lower()
                    if theverylargevariablenamerepresentingayesorno != 'y' and theverylargevariablenamerepresentingayesorno != 'yes':
                        print(f'ok u can leave, bye bye')
                        sys.exit(0)
                except KeyboardInterrupt:
                    print(f'ok u can leave, bye bye')
                    sys.exit(0)
                if theverylargevariablenamerepresentingayesorno == 'y':
                    print(f'ok, use the -s / --skip-file-exist to ignore this')

        try:
            with open(args.compile_output, 'w') as _:
                # just create the file to try catch now
                pass
        except FileNotFoundError:
            print(f'file "{args.compile_output}" does not exist')
            sys.exit(1)

        tea_interp.compile(args.compile_output)

if __name__ == '__main__': 
    runasfastaspossiblebutitspythonsoitsokifitsalittleslow()