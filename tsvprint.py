import os
import re
import time 
import random
import argparse

# str2bool type for argparse
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# get arguments
parser = argparse.ArgumentParser('tsvprint')
parser.add_argument('--file', type=str)

parser.add_argument('--head', type=int, default=-1, help='-1 to print all.')
parser.add_argument('--tail', type=int, default=-1, help='-1 to print all.')
parser.add_argument('--print_interval', type=float, default=-1, help='-1 to print once.')

parser.add_argument('--header_freq', type=int, default=-1, help='-1 not to print header in the middle.')
parser.add_argument('--float_prec', type=int, default=5)
parser.add_argument('--float_max_len', type=int, default=11)
parser.add_argument('--of_handling', type=str2bool, default=False)
args = parser.parse_args()

# assertion to handle not enough max length
# Example: for float_prec=5, minimum length float string should be -0.00000
assert args.float_max_len - args.float_prec - 2 > 0, "not enough float_max_len."

# to determine whether to use e format
# Example: for float_prec=5, float_max_len=11,
# (-10000.00000, -0.00001] and [0.00001, 10000.00000)
float_max = float('1e+{}'.format(args.float_max_len - args.float_prec - 2))
float_min = float('1e-{}'.format(args.float_prec))

# regex for detecting integer and float
check_int = re.compile('[-+]?[0-9]+$')
check_float = re.compile('[-+]?[0-9]+\.[0-9]+([eE][-+]?[0-9]+)?$')

line_count = 0

# check modification time and get lines
mtime = os.path.getmtime(args.file)
with open(args.file, 'r') as f:
    lines = f.readlines()
    printed_lines_num = len(lines)

    # get header
    header = lines[0].strip().split('\t')
    lines = lines[1:]

    # select necessary lines
    if args.head > 0:
        lines = lines[:args.head]
    elif args.tail > 0:
        lines = lines[-args.tail:]


    # get data type from first line
    data_type = []

    first_line = lines[0].strip().split('\t')

    for comp in first_line:
        if check_int.match(comp):
            data_type.append('int')

        elif check_float.match(comp):
            data_type.append('float')

        else:
            data_type.append('string')

    # compute max length for each component
    max_len = [len(h) for h in header]

    for line in lines:
        split_line = line.strip().split('\t')
        
        for idx, comp in enumerate(split_line):
            length = len(comp)

            if data_type[idx] == 'float':
                # length depends on float formatting
                if float_min <= float(comp) and float(comp) < float_max:
                    length = len(comp.split('.')[0]) + 1 + args.float_prec
                elif -float_max < float(comp) and float(comp) <= -float_min:
                    length = len(comp.split('.')[0]) + 1 + args.float_prec
                elif args.of_handling:
                    length = 7 + args.float_prec
                elif float(comp) >= float_max:
                    length = 3 # inf
                elif float(comp) <= -float_max:
                    length = 4 # -inf
                else:
                    length = len(comp.split('.')[0]) + 1 + args.float_prec # 0.000

            if length > max_len[idx]:
                max_len[idx] = length


    # make header string and print header
    header_str = ('| ' + ' | '.join(['{{:>{}}}'.format(length) for length in max_len]) + ' |').format(*header)
    print('-'*len(header_str))
    print(header_str)
    print('-'*len(header_str))

    # print formatted lines
    for line in lines:
        split_line = line.strip().split('\t')
        format_str = []

        for idx, dtype in enumerate(data_type):
            if dtype == 'int':
                # str to int
                split_line[idx] = int(split_line[idx])
                # make format string
                format_str.append('{{:{}}}'.format(max_len[idx]))
            elif dtype == 'string':
                # make format string
                format_str.append('{{:>{}}}'.format(max_len[idx]))
            elif dtype == 'float':
                # str to float
                split_line[idx] = float(split_line[idx])
                # make format string
                if float_min <= float(split_line[idx]) and float(split_line[idx]) < float_max:
                    format_str.append('{{:{}.{}f}}'.format(max_len[idx], args.float_prec))
                elif -float_max < float(split_line[idx]) and float(split_line[idx]) <= -float_min:
                    format_str.append('{{:{}.{}f}}'.format(max_len[idx], args.float_prec))
                elif args.of_handling:
                    format_str.append('{{:{}.{}e}}'.format(max_len[idx], args.float_prec))
                elif float(split_line[idx]) >= float_max:
                    split_line[idx] = 'inf'
                    format_str.append('{{:>{}}}'.format(max_len[idx])) # inf
                elif float(split_line[idx]) <= -float_max:
                    split_line[idx] = '-inf'
                    format_str.append('{{:>{}}}'.format(max_len[idx])) # -inf
                else:
                    format_str.append('{{:{}.{}f}}'.format(max_len[idx], args.float_prec)) # 0.000

        format_str = ('| ' + ' | '.join(format_str) + ' |')

        # print header for certain frequency
        line_count += 1
        if args.header_freq > 0 and line_count % args.header_freq == 0:
            print('-'*len(header_str))
            print(header_str)
            print('-'*len(header_str))

        print(format_str.format(*split_line))

# coutinue printing when the file is modified
if args.print_interval > 0:
    while True:
        # check if the file is modified
        if os.path.getmtime(args.file) > mtime:
            # store modification time
            mtime = os.path.getmtime(args.file)

            # print added line
            with open(args.file, 'r') as f:
                lines = f.readlines()
                lines2print = lines[printed_lines_num:]
                printed_lines_num = len(lines)

                for line in lines2print:
                    split_line = line.strip().split('\t')
                    format_str = []

                    for idx, dtype in enumerate(data_type):
                        if dtype == 'int':
                            # str to int
                            split_line[idx] = int(split_line[idx])
                            # make format string
                            format_str.append('{{:{}}}'.format(max_len[idx]))
                        elif dtype == 'string':
                            # make format string
                            format_str.append('{{:>{}}}'.format(max_len[idx]))
                        elif dtype == 'float':
                            # str to float
                            split_line[idx] = float(split_line[idx])
                            # make format string
                            if float_min <= float(split_line[idx]) and float(split_line[idx]) < float_max:
                                format_str.append('{{:{}.{}f}}'.format(max_len[idx], args.float_prec))
                            elif -float_max < float(split_line[idx]) and float(split_line[idx]) <= -float_min:
                                format_str.append('{{:{}.{}f}}'.format(max_len[idx], args.float_prec))
                            elif args.of_handling:
                                format_str.append('{{:{}.{}e}}'.format(max_len[idx], args.float_prec))
                            elif float(split_line[idx]) >= float_max:
                                split_line[idx] = 'inf'
                                format_str.append('{{:>{}}}'.format(max_len[idx])) # inf
                            elif float(split_line[idx]) <= -float_max:
                                split_line[idx] = '-inf'
                                format_str.append('{{:>{}}}'.format(max_len[idx])) # -inf
                            else:
                                format_str.append('{{:{}.{}f}}'.format(max_len[idx], args.float_prec)) # 0.000

                    format_str = ('| ' + ' | '.join(format_str) + ' |')

                    # print header for certain frequency
                    line_count += 1
                    if args.header_freq > 0 and line_count % args.header_freq == 0:
                        print('-'*len(header_str))
                        print(header_str)
                        print('-'*len(header_str))

                    print(format_str.format(*split_line))

        time.sleep(args.print_interval)

