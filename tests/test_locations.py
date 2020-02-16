#!/usr/bin/env python

# Author @vsoch, Written February 2020
# Read in the locations.csv and location-lookup.tsv files to validate each entry

import csv
import os
import pytest
import re
import requests
from time import sleep
from geopy.geocoders import Nominatim

here = os.path.dirname(os.path.abspath(__file__))


def read_rows(filepath, newline="", delim=","):
    """read in the data rows of a csv file.
    """
    # Read in the entire membership counts
    with open(filepath, newline=newline) as infile:
        reader = csv.reader(infile, delimiter=delim)
        data = [row for row in reader]
    return data


def get_sheet_data():
    """return Google sheets institution lookup
    """
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
    return [x.lower().strip() for x in lines[1:] if x.strip()]


def test_locations_lookup(tmp_path):
    """The locations-lookup.tsv file is a tab separated file of locations.
       Specifically, we need to ensure that it's in alphabetical order,
       and each has a city state that returns a location.
       The only other option is for a location to be remote, in which case,
       it is skipped. 
    """
    filepath = os.path.join(os.path.dirname(here), "_data", "location-lookup.tsv")
    assert os.path.exists(filepath)
    lines = read_rows(filepath, delim="\t")

    # These are to skip, don't know what they mean
    skips = ["llnsâ\\x80¯llc"]

    # 1. Ensure header is correct
    print("1. Testing for correct header with 'name' and 'city-state'")
    assert lines[0][0] == "name"
    assert lines[0][1] == "city-state"

    # 2. must be all lowercase, in abc order
    print("2. Names must be all lowercase and in alphabetical order.")
    names = [x[0].lower() for x in lines[1:]]
    comparator = list(set(x[0] for x in lines[1:]))
    comparator.sort()
    for i in range(len(names)):
        assert comparator[i] == names[i]

    # 3. All locations in lookup must be in actual data
    print("3. All locations in lookup must be in actual data.")
    data = get_sheet_data()
    for line in lines[1:]:
        name = line[0]
        if name in skips:
            continue
        assert name in data

    # 4. Ensure that each location has a lat and long
    print("4. Testing that each location has a latitude and longitude.")
    geolocator = Nominatim(user_agent="us-rse.org")
    for line in lines[1:]:
        name = line[0]
        address = line[1]
        print("Testing %s" % name)

        if name in skips:
            continue

        if address == "remote":
            print("%s is considered remote." % address)
            continue

        location = geolocator.geocode(address)
        sleep(1.5)
        assert location

    print("*Use preview on CircleCI to ensure that locations found are correct*")


def test_locations(tmp_path):
    """The locations.csv file is a comma separated file of locations.
       Each should have a name (lowercase), latitude, and longitude.
    """
    filepath = os.path.join(os.path.dirname(here), "_data", "locations.csv")
    assert os.path.exists(filepath)
    lines = read_rows(filepath)

    # 1. Check that header is correct
    print("1. Checking that header has name, lat, lng, count")
    header = lines.pop(0)
    assert header[0] == "name"
    assert header[1] == "lat"
    assert header[2] == "lng"
    assert header[3] == "count"

    # 2. Check that name is all lowercase
    print("Checking names, latitudes, longitudes, and counts != 0")
    for line in lines:
        name = line[0]
        lat = line[1]
        lng = line[2]
        count = line[3]

        print("Testing %s" % name)
        assert name.lower() == name
        assert float(lat)
        assert float(lng)
        assert int(count)
        assert int(count) != 0
