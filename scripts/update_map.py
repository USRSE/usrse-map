#!/usr/bin/env python3

# Update map will retrieve locations via a csv, and then generate a new yaml file using lookup of schools
# https://docs.google.com/spreadsheets/d/1FTnl8ucFKYtiS2xhNiK8VwXeE5BuBDCzL_k9SbqyG6A/edit#gid=1109363929
# requests is required
# Copyright @vsoch, 2020

from geopy.geocoders import Nominatim

# from uszipcode import SearchEngine

import json
import requests
import shutil
import sys

import os
import csv
import requests
import shutil
import sys
import tempfile

here = os.path.dirname(os.path.abspath(__file__))


def get_filepath():
    """get path for the data file to write
    """
    return os.path.join(os.path.dirname(here), "_data", "locations.csv")


def get_lookup():
    """get path for the locations lookup file.
    """
    filepath = os.path.join(os.path.dirname(here), "_data", "location-lookup.tsv")
    if not os.path.exists(filepath):
        sys.exit("Cannot find %s" % filepath)
    return filepath


def read_rows(filepath, newline="", delim=","):
    """read in the data rows of a csv file.
    """
    # Read in the entire membership counts
    with open(filepath, newline=newline) as infile:
        reader = csv.reader(infile, delimiter=delim)
        data = [row for row in reader]
    return data


def main():
    """main entrypoint for the script to generate the locations file
    """

    # A tsv download for just the worksheet with summary counts
    sheet = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTBn_kgBH8WoFmqdRJYdw8GrmfvjbdWIMYCk-yxelaE8aUO3J0rY19_wPOI9HHW0U0tc5Bg19uApPzx/pub?gid=145007959&single=true&output=tsv"

    # Ensure the response is okay
    response = requests.get(sheet)
    if response.status_code != 200:
        print(
            "Error with getting sheet, response code %s: %s"
            % (response.status_code, response.reason)
        )
        sys.exit(1)

    # Split lines by all sorts of fugly carriage returns
    lines = response.text.split("\r\n")

    # Remove empty responses, header row, make all lowercase
    lines = [x.lower().strip() for x in lines[1:] if x.strip()]

    # Read the location lookup file
    lookup_rows = read_rows(get_lookup(), delim="\t")

    # Remove header (should have name and city-state)
    assert lookup_rows[0][0] == "name"
    assert lookup_rows[0][1] == "city-state"
    lookup_rows.pop(0)

    # Create lookup dictionary
    lookup = {x[0]: x[1] for x in lookup_rows}

    # Create geolocator and search engine
    geolocator = Nominatim(user_agent="us-rse.org")
    # search = SearchEngine(simple_zipcode=True)

    # Get lats/long for each location, keep track of missing
    latlong = dict()
    missing = set()
    for name, address in lookup.items():

        # Skip remote addresses
        if address == "remote":
            continue

        print("Looking up %s in %s" % (name, address))
        # Second shot, try for international address

        location = geolocator.geocode(address)
        if location:
            lat = location.latitude
            lng = location.longitude
            latlong[name] = [lat, lng]
        else:
            print("%s: %s is not found with geocoding." % (name, address))
            missing.add(name)

    # Keep track of locations not known, counts known
    unknown = set()
    counts = {}

    for line in lines:
        if line not in lookup:
            unknown.add(line)
            continue
        if line not in counts:
            counts[line] = 0
        counts[line] += 1

    # Generate list of names with latitude and longitude for each
    # [name, lat, long, count]
    locations = [["name", "lat", "lng", "count"]]
    for name in lines:

        # We found a location (lat long) for the place!
        if name in latlong and name in counts:
            locations.append([name, latlong[name][0], latlong[name][1], counts[name]])

    print("Found a total of %s locations, each with a count!" % (len(locations) - 1))

    # We will write results to this file
    filepath = get_filepath()

    # Write the new file
    with open(filepath, "w", newline="") as outfile:
        writer = csv.writer(outfile, delimiter=",")
        [writer.writerow(row) for row in locations]

    print("Wrote locations and counts to %s." % filepath)


if __name__ == "__main__":
    main()
