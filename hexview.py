#!/usr/bin/env python3
import argparse


def read_file(filename, nbytes, sbytes):
    with open(filename, "rb") as f:
        f.seek(sbytes)
        file = f.read(nbytes)
    return file


def get_char(byte):
    if 32 <= byte <= 126:
        return chr(byte)
    else:
        return '.'


def print_canonical(file, address):
    row = 0
    ascii_line = []
    for c in file:
        if row == 0:
            print('{:07x} '.format(address), end=" ")

        print('{:02x}'.format(c), end=" ")
        ascii_line.append(get_char(c))
        row += 1
        if row == 8:
            print(' ', end='')

        if row == 16:
            print(' |{}|'.format(''.join(ascii_line)))
            ascii_line = []
            row = 0
        address += 1

    # if the output doesn't end on a full row, we need to
    # pad with some spaces so the string representation
    # aligns properly
    if row != 00:
        padding = 16 - row
        if row < 8:
            extra_space = ' '
        else:
            extra_space = ''
        print('   ' * padding + extra_space, end='')
        print(' |{}|'.format(''.join(ascii_line)))


def main(args):
    for f in args.filename:
        file = read_file(f, args.n, args.s)
        print_canonical(file, args.s)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='hexview.py', usage='%(prog)s filename')

    parser.add_argument('filename', help="The file you wish to hexdump", nargs='*')
    parser.add_argument('-n', help="Output n bytes of output", type=int)
    parser.add_argument('-s', help="Skip n bytes", type=int, default=0)

    args = parser.parse_args()

    main(args)
