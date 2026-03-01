import argparse
import logging

from interpreter import Teaterpreter

from tokenizing.keywords import *
from tokenizing.operators import *

from export.compiler import Compiler

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

    # create compilation argument group
    compilation_group = argp.add_argument_group(title='compiling', description='arguments related to compiling the program')
    compilation_group.add_argument('-c', '--compile', action='store_true', help='whether to compile the given file', dest='compile')
    compilation_group.add_argument('-o', '--output', type=str, help='where to write compiled file to, defaults to stdout', dest='output')

    args = argp.parse_args()

    # setup logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(encoding='utf-8', level=args.log_level, format='[%(asctime)s] [%(filename)s:%(lineno)s:%(name)s] [%(levelname)s] %(message)s', datefmt='%s')

    # setup the tea
    tea_interp = Teaterpreter(args.file_name)

    if args.compile:
        nodes = tea_interp.nodeify()
        compiled = Compiler(nodes).compile()
        if args.output == None:
            print(compiled.decode())
        else:
            with open(args.output, 'wb') as f:
                f.write(compiled)

            logger.info('finished compilation with zero issues')
    else:
        processed = tea_interp.nodeify()

if __name__ == '__main__': 
    runasfastaspossiblebutitspythonsoitsokifitsalittleslow()