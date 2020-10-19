import argparse
import datetime
from os import path
import sys
import logging

parser = argparse.ArgumentParser(description='split file content to n number of files of similar interval', add_help=False)
parser.add_argument('-h','--help', action='help', help='Example: python split_to_multiple_files.py -i input_file.txt -n 10')
parser.add_argument('-i', '--input', required=True, help='input file')
parser.add_argument('-n', '--number', default='5', help='interval (default 5)')

args = parser.parse_args()

input_file = ''
n = 5


if path.exists(args.input):
    input_file = path.abspath(args.input)
else:
    print('\ninput file not found for -i parameter!\n')
    parser.print_help(sys.stderr)
    sys.exit(1)

try:
    n = int(args.number)
except ValueError:
    print('\ninvalid int value for -n parameter!\n')
    parser.print_help(sys.stderr)
    sys.exit(1)

outfile = 'split_file.log'

logger = logging.getLogger('split_file.log')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(outfile)
fh.setLevel(level=logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.info('start time: '+str(datetime.datetime.now()))

lines = []

with open(input_file, 'r') as inp:
    lines = inp.read().splitlines()

temp_out = []
file_count = 0

for i, ip in enumerate(lines):
    
    print(str(i))
    print(f'{ip}')
    
    logger.info(f'{ip}')
    
    if i == 0:
        temp_out.append(ip)
        
    elif i == len(lines)-1:
        temp_out.append(ip)
        
        print(f'building up output file {file_count+1}\n')
        logger.info(f'building up output file {file_count+1}\n')
        
        with open(f'output_{file_count+1}.txt', 'w') as out_file:
            for temp in temp_out:
                out_file.write(f'{temp}\n')

        print(f'written ips to output_{file_count+1}.txt\n')
        logger.info(f'written ips to output_{file_count+1}.txt\n')
        
    elif i%n == 0:
        print(f'building up output file {file_count+1}\n')
        logger.info(f'building up output file {file_count+1}\n')
        
        with open(f'output_{file_count+1}.txt', 'w') as out_file:
            for temp in temp_out:
                out_file.write(f'{temp}\n')

        print(f'written ips to output_{file_count+1}.txt\n')
        logger.info(f'written ips to output_{file_count+1}.txt\n')

        del temp_out[:]
        temp_out.append(ip)
        file_count = file_count + 1
    else:
        temp_out.append(ip)

logger.info('end time: '+str(datetime.datetime.now()))
logging.shutdown()
