#!/usr/bin/python3
# Author: Jeremiah Bess

# Imports
import argparse
from os import path
from math import ceil

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
    filepath, filename = path.split(file)
    basename, ext = path.splitext(filename)
    if filepath == '':
        fileprefix = f'{basename}' # Handle local relative paths
    else:
        fileprefix = f'{filepath}/{basename}'

    # Calculate and create splits
    if ext == '.csv':
        csvheader = data[0]
        splitstart = 1 # Starting slice for data excluding header
        splitmax -= 1 # Remove header from split count
        splitstop = splitmax + 1 # Stopping slice for data
    else:
        csvheader = ''
        splitstart = 0 # Starting slice for data
        splitstop = splitmax  # Stopping slice for data
    splits = ceil(len(data) / splitmax)  # Count of splits always rounded up
    splitnum = 1 # Used for filename

    while splitnum <= splits:
        if data[splitstart:splitstop] == []:
            break
        newfilename = f'{fileprefix}-{splitnum}{ext}'
        with open(newfilename, 'w') as f:
            if csvheader:
                f.write(csvheader)
            for line in data[splitstart:splitstop]:
                f.write(line)
        splitstart = splitstop # Reset start where we ended
        splitstop = splitstop + splitmax # Set next splitmax (added to itself)
        splitnum += 1 # Increment filename split number
        
# Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Splits text file by specified line count')
    parser.add_argument('file', help='Full or relative path to file to split')
    parser.add_argument('lines', type=int, help='Maximum number of lines in each split file')

    args = parser.parse_args()

    splitFile(args.file, args.lines)
