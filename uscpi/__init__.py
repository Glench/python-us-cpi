# Glen Chiacchieri, 2013
import urllib2
import datetime
import tempfile
from decimal import Decimal
import re
import shutil
import csv

def in_range(value, smallest, largest):
    return value >= smallest and value <= largest

def assert_in_range(value, smallest, largest, name):
    assert in_range(value, smallest, largest), '{} ({}) must be in range {}-{}' \
        .format(name, value, smallest, largest)

def average(some_list):
    return sum(some_list) / len(some_list)

class UsCpi(object):
    """Tools for manipulating the US CPI (all urban consumers)."""
    url = 'ftp://ftp.bls.gov/pub/special.requests/cpi/cpiai.txt'
    start_line = 19 # line that the data from the txt file starts on
    csv_file = None
    first_year = None
    last_year = None
    normalized_years = {}
    headers = [
        'Year',
        'Jan.',
        'Feb.',
        'Mar.',
        'Apr.',
        'May',
        'June',
        'July',
        'Aug.',
        'Sep.',
        'Oct.',
        'Nov.',
        'Dec.',
        'Annual Avg.',
        'Percent change Dec-Dec',
        'Percent change Avg-Avg',
    ]
    raw_separator_re = re.compile(r'(\w\.?)(\s+)(-?\w)')

    def __init__(self):
        self.csv_file = self.raw_to_csv(self.get())
        self.process_csv(self.csv_file)

    def get(self, outfile=None):
        """Return the data as a urllib2 response object."""
        return urllib2.urlopen(self.url)

    def raw_to_csv(self, raw_file):
        """
        Convert the raw text file to a CSV file and return it.
        """
        csv_file = tempfile.NamedTemporaryFile()
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(self.headers)
        for i, line in enumerate(raw_file):
            if i >= self.start_line and self.raw_separator_re.search(line):
                with_commas = self.raw_separator_re.sub(r'\1,\3', line).strip()
                csv_file.write(with_commas)
                csv_file.write('\n')
        # cursor is at the end of the file, move it back to beginning
        csv_file.seek(0)
        return csv_file

    def process_csv(self, csv_file):
        """
        Reads and normalizes the CSV data for later lookup.
        """
        for i, row in enumerate(csv.reader(csv_file)):
            if i != 0:
                # create index of year -> avg cpi for that year
                if i == 1:
                    # mark first year of data
                    self.first_year = int(row[0])
                try:
                    # this uses the government's CPI average for the year
                    self.normalized_years[int(row[0])] = Decimal(row[13])
                except IndexError:
                    # if there isn't an average for the year yet, average the
                    # data that we have so far for the year
                    self.normalized_years[int(row[0])] = \
                        average([Decimal(cpi) for cpi in row[1:12]])
        # mark last year of data
        self.last_year = int(row[0])
        # cursor is at the end of the file, move it back to beginning
        csv_file.seek(0)

    def as_csv(self, outfile_path):
        """
        Write the csv data to a given file.
        """
        with open(outfile_path, 'wb') as csv_outfile:
            shutil.copyfileobj(self.csv_file, csv_outfile)
            # cursor is at the end of the file, move it back to beginning
            self.csv_file.seek(0)

    def cpi_for_year(self, year):
        """
        Get the CPI for a given integer year.
        """
        return self.normalized_years[year]

    def inflation_factor(self, base_year, inflation_year):
        """
        Return a float inflation factor. This can be used to multiply the
        value for the base year to find the value in the inflation year.

        You can read this as 'inflation factor when converting base_year
        dollars into inflation_year dollars'.
        """
        base_cpi = self.cpi_for_year(base_year)
        inflation_cpi = self.cpi_for_year(inflation_year)
        return inflation_cpi / base_cpi

    def value_with_inflation(self, base_amount, base_year, inflation_year=None):
        """
        Returns the purchasing power of <base_amount> (from <base_year>)
        in <inflation_year> (default is last year in data, likely the current
        year).

        Uses averages over years to calculate. If it's the middle of the year
        and there isn't CPI data for all months, will use a calculated average
        for the year so far.
        """
        inflation_year = inflation_year or self.last_year

        # error checking
        assert_in_range(base_year, self.first_year, self.last_year, 'base year')
        assert_in_range(inflation_year, self.first_year, self.last_year, 'inflation year')
        if not isinstance(base_amount, Decimal):
            base_amount = Decimal(str(base_amount))
        return round(Decimal(base_amount * self.inflation_factor(base_year, inflation_year)), 2)

if __name__ == '__main__':
    import sys
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = 'us_cpi_{}.csv'.format(datetime.date.today().isoformat())
    print 'Downloading file...'
    cpi = UsCpi()
    cpi.as_csv(filename)
    print 'Done. CSV written to', filename
