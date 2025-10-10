import argparse
import logging

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

    args = argp.parse_args()

    # setup logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(encoding='utf-8', level=args.log_level, format='[%(asctime)s] [%(filename)s:%(lineno)s:%(name)s] [%(levelname)s] %(message)s', datefmt='%s')

    # setup the tea
    tea_interp = Teaterpreter(args.file_name)

    processed = tea_interp.process()

if __name__ == '__main__': 
    runasfastaspossiblebutitspythonsoitsokifitsalittleslow()