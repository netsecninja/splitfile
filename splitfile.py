#!/usr/bin/python3
# Author: Jeremiah Bess

# Imports
import argparse

# Globals

# Functions
def splitFile(file, splitmax):
    # Open file and gather contents
    try:
        f = open(file)
    except OSError as e:
        print(e)
        return
    with f:
        data = f.readlines()

    # Parse out path and filename
    from os import path
    filepath, filename = path.split(file)
    basename, ext = path.splitext(filename)
    if filepath == '':
        fileprefix = f'{basename}' # Handle local relative paths
    else:
        fileprefix = f'{filepath}/{basename}'

    # Calculate and create splits
    splits = int(len(data)/splitmax) + 1 # Count of splits rounded up
    splitstart = 0 # Starting slice for data
    splitstop = splitmax # Stopping slice for data
    splitnum = 1 # Used for filename

    while splitnum <= splits:
        newfilename = f'{fileprefix}-{splitnum}{ext}'
        with open(newfilename, 'w') as f:
            for line in data[splitstart:splitstop]:
                f.write(line)
        splitstart = splitstop + 1 # Reset start where we ended
        splitstop = splitstop + splitmax + 1 # Set next splitmax (added to itself)
        splitnum += 1 # Increment filename split number
        
# Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Splits text file by specified line count')
    parser.add_argument('file', help='Full or relative path to file to split')
    parser.add_argument('lines', type=int, help='Maximum number of lines in each split file')

    args = parser.parse_args()

    splitFile(args.file, args.lines)
