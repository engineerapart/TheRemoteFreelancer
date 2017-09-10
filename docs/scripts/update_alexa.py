#!python3
"""
This script updates the alexa rankings in the csv file.
Usage:

    python3 update_alexa.py
"""

import csv
import sys
import os

import alexa

sites_path = os.path.join(os.path.dirname(__file__), "..", "_data", "sites.csv")

update_blank_only = os.environ.get("update_blank_only", "false") == "true"


def main():
    with open(sites_path, 'r') as csvfile:
        links = list(csv.DictReader(csvfile))
    for link in links:
        if link['rank'] and update_blank_only:
            continue
        print("Updating {}.. ".format(link['netloc']), end="")
        sys.stdout.flush()
        rank = alexa.get_rank(link['netloc'])
        if rank:
            link['rank'] = alexa.add_commas_to_rank(alexa.round_rank(rank))
            print(link['rank'])
    with open(sites_path, 'w') as csvfile:
        fieldnames = list(links[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(links)


if __name__ == "__main__":
    main()
