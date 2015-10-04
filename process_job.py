"""
    Scrapie Job Processor
    Copyright 2015 - Carter Yagemann
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import config
from lxml import html
import requests
import time
import json
import sys

if __name__ == "__main__":
    # Get job from file
    if len(sys.argv) < 2:
        sys.exit("Insufficient arguments")
    
    filename = sys.argv[1]
    file = open(filename, "r")
    job = json.loads(file.read())
    file.close()
    
    # Fetch HTML page
    page = requests.get(job[0]['url'])
    tree = html.fromstring(page.text)
    # Scrape data
    date = time.strftime("%m/%d/%Y-%H%M%S")
    data = []
    for i in range(1, len(job)):
        try:
            value = tree.xpath('//' + job[i]['element'] + '[@' + job[i]['attribute'] + '="' + job[i]['value'] + '"]/text()')[0].strip()
            data.append(value)
        except:
            print "Failed to scrape", job[i]['value']
    # Write to file
    output = open(filename.replace(config.job_dir, config.data_dir).replace(".job", ".csv"), "a")
    output.write(date + ', ')
    for i in range(len(data) - 1):
        output.write(data[i] + ', ')
    output.write(data[len(data) - 1] + '\n')
    output.close()
