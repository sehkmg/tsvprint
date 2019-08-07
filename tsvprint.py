import argparse
import random
import re

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
parser.add_argument('--file_name', type=str)
parser.add_argument('--float_prec', type=int, default=3)
parser.add_argument('--float_max_len', type=int, default=10)
parser.add_argument('--head', type=int, default=-1, help='-1 to print all.')
parser.add_argument('--tail', type=int, default=-1, help='-1 to print all.')
args = parser.parse_args()

# assertion to handle not enough max length
# Example: for float_prec=3, minimum length float string should be -0.000
assert args.float_max_len - args.float_prec - 2 > 0, "not enough float_max_len."

# to determine whether to use e format
# Example: for float_prec=3, float_max_len=9,
# (-10000.000, -0.001] and [0.001, 10000.000)
float_max = float('1e+{}'.format(args.float_max_len - args.float_prec - 2))
float_min = float('1e-{}'.format(args.float_prec))

# regex for detecting integer and float
check_int = re.compile('[-+]?[0-9]+$')
check_float = re.compile('[-+]?[0-9]+\.[0-9]+([eE][-+]?[0-9]+)?$')


# get lines
with open(args.file_name, 'r') as f:
    lines = f.readlines()

    # get header
    header = lines[0].strip().split('\t')
    lines = lines[1:]

    # select necessary lines
    if args.head > 0:
        lines = lines[:args.head]
    elif args.tail > 0:
        lines = lines[-args.tail:]


    # get data type and float formatting from random line
    data_type = []

    ran_idx = random.randint(0, len(lines)-1)
    random_line = lines[ran_idx].strip().split('\t')

    for comp in random_line:
        if check_int.match(comp):
            data_type.append(('int', True))

        elif check_float.match(comp):
            if float_min <= float(comp) and float(comp) < float_max:
                data_type.append(('float', True))
            elif -float_max < float(comp) and float(comp) <= -float_min:
                data_type.append(('float', True))

            else:
                data_type.append(('float', False))

        else:
            data_type.append(('string', True))

    # compute max length for each component
    max_len = [len(h) for h in header]

    for line in lines:
        split_line = line.strip().split('\t')
        
        for idx, comp in enumerate(split_line):
            length = len(comp)

            if data_type[idx][0] == 'float':
                if data_type[idx][1]:
                    length = len(comp.split('.')[0]) + 4
                else:
                    length = 7 + args.float_prec

            if length > max_len[idx]:
                max_len[idx] = length

    # make format string
    format_str = []

    for idx, dtype in enumerate(data_type):
        if dtype[0] == 'int':
            format_str.append('{{:{}}}'.format(max_len[idx]))
        elif dtype[0] == 'string':
            format_str.append('{{:>{}}}'.format(max_len[idx]))
        elif dtype[0] == 'float':
            if dtype[1]:
                format_str.append('{{:{}.{}f}}'.format(max_len[idx], args.float_prec))
            else:
                format_str.append('{{:{}.{}e}}'.format(max_len[idx], args.float_prec))

    format_str = ('| ' + ' | '.join(format_str) + ' |')


    # make header string and print header
    header_str = ('| ' + ' | '.join(['{{:>{}}}'.format(length) for length in max_len]) + ' |').format(*header)
    print(header_str)
    print('-'*len(header_str))

    # print formatted lines
    for line in lines:
        split_line = line.strip().split('\t')

        for idx, dtype in enumerate(data_type):
            if dtype[0] == 'int':
                split_line[idx] = int(split_line[idx])
            elif dtype[0] == 'float':
                split_line[idx] = float(split_line[idx])

        print(format_str.format(*split_line))
