#!python3
"""
This script updates the alexa rankings and sort the csv file.
Usage:

    python3 update.py
"""

import csv
import sys
import os
import itertools
import math

import alexa
from download_favicons import download_favicons

sites_path = os.path.join(os.path.dirname(__file__), "..", "_data", "sites.csv")

update_blank_only = os.environ.get("update_blank_only", "false") == "true"


def add_commas_to_rank(number):
    if number:
        if isinstance(number, str):
            number = remove_commas(number)
        return "{:,}".format(number)


def round_rank(rank: int):
    return round(rank, 1 - (1 + int(math.log10(abs(rank)))))


def remove_commas(string_number):
    return int(string_number.replace(",", ""))


def update_alexa(links):
    for link in links:
        link['rank'] = add_commas_to_rank(link['rank'])
        if link['rank'] and update_blank_only:
            continue
        print("Updating {}.. ".format(link['netloc']), end="")
        sys.stdout.flush()
        rank = alexa.get_rank(link['netloc'])
        if rank:
            link['rank'] = add_commas_to_rank(round_rank(rank))
            print(link['rank'])
    return links


def get_groups(links):
    links.sort(key=lambda _: _['section'])
    for group_name, group_data in itertools.groupby(links, lambda _: _['section']):
        group_data = list(group_data)
        group_data.sort(key=lambda _: remove_commas(_['rank']))
        yield group_name, group_data


def get_groups_in_order(links):
    rank_sorted_groups = dict(get_groups(links))
    for group in ["Clients", "Tutoring", "Other", "Agency"]:
        yield from rank_sorted_groups[group]


def sort(links):
    return list(get_groups_in_order(links))


def main(func):
    with open(sites_path, 'r') as csvfile:
        links = list(csv.DictReader(csvfile))
    links = func(links)
    if not links:
        return
    with open(sites_path, 'w') as csvfile:
        fieldnames = list(links[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(links)


if __name__ == "__main__":
    main(update_alexa)
    main(sort)
    main(download_favicons)
