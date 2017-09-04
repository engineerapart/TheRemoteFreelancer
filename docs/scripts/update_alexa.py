#!python3
"""
This script updates the alexa rankings in the csv file.
Usage:

    python3 update_alexa path/to/data.csv
"""

import csv
import sys

def main(input_rows):
	yield from input_rows

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print(__doc__)
		exit(1)
	with open(sys.argv[1], 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		output = list(main(reader))
	with open(sys.argv[1], 'w') as csvfile:
		fieldnames = list(output[0].keys())
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(output)
