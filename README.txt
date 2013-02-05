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

    $: python uscpi/__init__.py [filename]

The command line version will output a CSV file of the latest US Consumer Price Index, taken from the this site: http://www.bls.gov/cpi/#tables

This tool also comes with an inflation calculator as demonstrated in the python example above.
