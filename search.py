#!/usr/bin/env python3

import csv
import sys
import json

################################################################################
# Search the CSV file for the given search terms
################################################################################
def search_csv_file(*search_terms):
    rows = []
    rows_primary = []
    rows_secondary = []

    with open('docs.csv', 'r', newline='') as file:

        reader = csv.DictReader(file)

        for row in reader:

            title = row['title'].lower()
            description = row['description'].lower()

            if search_terms is None:
                rows.append(row)

            elif all(term.lower() in title for term in search_terms):
                rows_primary.append(row)

            elif all(term.lower() in description for term in search_terms):
                rows_secondary.append(row)

    if len(rows_primary) > 0 or len(rows_secondary) > 0:
        rows = rows_primary + rows_secondary

    return rows

################################################################################
# Script entry point
################################################################################
if __name__ == '__main__':

    if len(sys.argv) > 1:
        search_terms = sys.argv[1:]
        results = search_csv_file(*search_terms)
    else:
        results = search_csv_file()
        results = results[:15]

    data = []

    for row in results:

        if '/docs/app/' in row['url']:
            title = f"{row['title']} [APP]"
        elif '/docs/pages/' in row['url']:
            title = f"{row['title']} [PAGES]"
        else:
            title = row['title']

        data.append({
            'title': title,
            'subtitle': row['description'],
            'arg': row['url']
        })

    data = json.dumps({ "items": data }, indent=2)
    print(data)
