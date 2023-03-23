#!/usr/bin/env python3

# Update map will retrieve locations via a csv, and then generate a new yaml file using lookup of schools
# requests is required
# Copyright @vsoch, 2020

from geopy.geocoders import Nominatim

# from uszipcode import SearchEngine

import requests
import sys

import os
import csv
import re
import time

here = os.path.dirname(os.path.abspath(__file__))


def get_filepath():
    """get path for the data file to write"""
    return os.path.join(os.path.dirname(here), "_data", "locations.csv")


def get_locations():
    """get path for the locations already found"""
    filepath = os.path.join(os.path.dirname(here), "_data", "locations.csv")
    if not os.path.exists(filepath):
        sys.exit("Cannot find %s" % filepath)
    return filepath


def get_location(geolocator, address, delay=1.5, attempts=3):
    """Retry to use the geolocator, fail after some number of attempts"""
    try:
        time.sleep(delay)
        location = geolocator.geocode(address, timeout=10)
        return location
    except:
        if attempts > 0:
            return get_location(
                geolocator, address, delay=delay + 1, attempts=attempts - 1
            )
        raise


def read_rows(filepath, newline="", delim=","):
    """read in the data rows of a csv file."""
    # Read in the entire membership counts
    with open(filepath, newline=newline) as infile:
        reader = csv.reader(infile, delimiter=delim)
        data = [row for row in reader]
    return data


def main():
    """main entrypoint for the script to generate the locations file"""
    # A csv download for just the worksheet with city, state
    sheet = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTBn_kgBH8WoFmqdRJYdw8GrmfvjbdWIMYCk-yxelaE8aUO3J0rY19_wPOI9HHW0U0tc5Bg19uApPzx/pub?gid=1918148706&single=true&output=csv"

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
    lines = [x.lower().strip('"').strip() for x in lines[1:] if x.strip()]

    # These locations we've already found
    locations = read_rows(get_locations(), delim=",")
    assert locations[0] == ["name", "lat", "lng", "count"]
    locations.pop(0)
    locations = {x[0]: x[1:] for x in locations}

    # Create geolocator and search engine
    geolocator = Nominatim(user_agent="us-rse.org")
    # search = SearchEngine(simple_zipcode=True)

    # Get lats/long for each location, keep track of missing
    missing = set()
    for address in lines:

        # Skip remote addresses
        if address in ["remote", "", None]:
            continue

        # Berkeley CA is also in candata
        if address == "berkeley, ca":
            address = "berkeley, california"

        if re.search(", ca$", address):
            print("Found %s, suggested to change to california" % address)

        if address not in locations:
            print("Looking up %s" % address)
            # Second shot, try for international address

            location = get_location(geolocator, address)

            # Rate limit is 1 per second
            if location:
                lat = location.latitude
                lng = location.longitude
                locations[address] = [lat, lng]
            else:
                print("%s is not found with geocoding." % address)
                missing.add(address)

    # Keep track of locations not known, counts known
    unknown = set()
    counts = {}

    # Now go through lines, but include each unique
    for line in lines:
        if line not in locations and line != "remote":
            unknown.add(line)
            continue
        if line not in counts:
            counts[line] = 0
        counts[line] += 1

    # Alert user about unknown locations
    print("UNKNOWN:\n %s\n" % "\n".join(unknown))
    print("MISSING:\n %s" % "\n".join(missing))

    # Sort counts
    counts = {
        k: v for k, v in sorted(counts.items(), reverse=True, key=lambda item: item[1])
    }

    # Generate list of names with latitude and longitude for each
    # [name, lat, long, count]
    seen = set()
    updated = [["name", "lat", "lng", "count"]]
    for name in lines:

        if name in seen:
            continue

        seen.add(name)

        # We found a location (lat long) for the place!
        if name in locations and name in counts and counts[name] > 0:
            updated.append([name, locations[name][0], locations[name][1], counts[name]])

    print("Found a total of %s locations, each with a count!" % (len(updated) - 1))

    # We will write results to this file
    filepath = get_filepath()

    # Write the new file
    with open(filepath, "w", newline="") as outfile:
        writer = csv.writer(outfile, delimiter=",")
        [writer.writerow(row) for row in updated]

    print("Wrote locations and counts to %s." % filepath)


if __name__ == "__main__":
    main()
