# The US-RSE Map

[![GitHub actions status](https://github.com/USRSE/usrse-map/workflows/CI/badge.svg?branch=master)](https://github.com/USRSE/usrse-map/actions?query=branch%3Amaster+workflow%3ACI)

This repository contains static files and workflows to generate the US-RSE map.

![assets/img/usrse-map.png](assets/img/usrse-map.png)

## How does it work?

#### Latest

We currently ask participants that fill out
the form to provide a city, town location if they want to anonymously be included in the
map. To minimize needing to use the geolocate API, we still write coordinates to the [locations data](_data/locations.csv) file. **You should not manually update this file** as it is done by a script (see below). 

#### June 2020 and Earlier

The map locations are derived from the US-RSE official roster, meaning
that the institutions or companies are exported. In the first implementation, institutions
were associated with a location by way of the [locations lookup](_data/location-lookup.tsv)
and then had matched latitude and longitude coordinates from the (now renamed)
[locations institutions data](_data/locations-institutions.csv).


### 1. How do I update the map?

You don't! The automated workflow does. The workflow under [.github/workflows/update-map.yml](.github/workflows/update-map.yml)
handles this for you. To add yourself (if you haven't yet) you can fill out the 
institution field under the [join form](https://docs.google.com/forms/d/e/1FAIpQLSdJbPczGHFN8mfMFu_YQym508OzFtOZxfSzr1sOoINxaMmiaw/viewform).

### 2. How do update locations?

The [locations lookup](_data/location-lookup.tsv) used to need monthly updating, but we don't
use it anymore. Look at older versions of this file under the repository version control
to see how this worked. 

### 3. How do we run tests?

Tests are run in a separate workflow at [.github/workflows/main.yml](.github/workflows/main.yml).
Since a contribution will come down to updating the list of locations, we ensure that
the fields and types are represented correctly.

<!--- ## Join us! --->

<a href="https://docs.google.com/forms/d/e/1FAIpQLScBQ6AYpYYK2wL21egcaVvH0ZEvtShU-0s-XbqnY3okUsyIZw/viewform">
<img width="250px" alt="signup button" src="assets/img/signup.png"></a> 
