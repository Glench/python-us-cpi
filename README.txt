=============
python-us-cpi
=============

Tools for parsing the latest US Consumer Price Index

To install::

    pip install UsCpi

or::

    easy_install UsCpi

Usage
=====

In python::

    from uscpi import UsCpi
    cpi = UsCpi() # downloads the latest CPI data

    # $100 in 2012 is worth how much in 1980?
    cpi.value_with_inflation(100, 2012, 1980)

or command line::

    user@computer:~$ python uscpi/__init__.py [filename]

The command line version will output a CSV file of the latest US Consumer Price Index, taken from this site: http://www.bls.gov/cpi/#tables

This tool also comes with an inflation calculator as demonstrated in the python example above.

Source is at Github: https://github.com/Glench/python-us-cpi

If you just want the CSV, you should be able to download the latest version here: http://glench.com/open-source/python-us-cpi/latest_us_cpi.csv
