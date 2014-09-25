Download Socrata Portals
======

This README is for downloading specific metadata for ingestion into [Plenario](https://github.com/UrbanCCD-UChicago/plenario), one data portal at a time. See the [original repo](https://github.com/tlevine/socrata-download) for a detailed README on the original functionality. This README only covers a small portion of the original functionality, as well as added features (`create_csv.py`) not originally included.

At the moment (Sep 2014) Plenario can only accept data with a geospatial (lat-long) and temporal (date) component. This script lets you quickly find *all* datasets on a given data portal that meet those criteria. 

### How to run (single data portal)

Say you want metadata for the City of Chicago data portal, which is located at <https://data.cityofchicago.org>. 

Add `SOCRATA_URL` to your `~/.bash_profile` and set it to a string representing the root URL (without `https://`). In our case this would look like 
`export SOCRATA_URL='data.cityofchicago.org'`

`cd` to the root folder and run `bash run_one.sh`.

This will run for a while downloading JSON metadata for every dataset on the City of Chicago data portal. 

When it finishes, open the `create_csv.py` file and change the `portal`, `outfile`, and `numfiles` variables as specified there. Then run `python create_csv.py`. This will create a tab-delimited text file in the `/data/data.cityofchicago.org` folder with the same name as `outfile`. Open that file in Excel or Google Sheets and filter for datasets that meet Plenario's criteria:

* `temporal field` has a value
* `geocoded` = 'Yes'
* `view type` = 'tabular'

You will need to use the provided dataset URL to gather information about the update frequency and ensure the dataset has a unique ID and that the dates have the proper interpretation (i.e., not `01/01/2014` standing in for the year `2014`).

The file structure and outfile for the City of Bristol data portal is left in as an example.

You may also be able to use the view IDs in `/rows-only/data` to write a script to hit a large number of Socrata data portals at once... if you want. 