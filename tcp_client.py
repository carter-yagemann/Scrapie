"""
    Scrapie Upload API
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
import SocketServer
import os
import json
import time

"""
Receives a JSON object describing a scraping job and turns it into a cronjob
for the scraper script.
"""
class TCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        # Process request
        result = self.processJson(self.data)
        if result == True:
            self.request.sendall("OKAY")
        else:
            self.request.sendall("FAILURE")
    
    def processJson(self, data):
        try:
            # Parse job
            job_json = json.loads(data)
            # Write job to file
            date = time.strftime("%m%d%Y-%H%M%S")
            job_filename = config.job_dir + "/" + date + ".job"
            file = open(job_filename, "w")
            file.write(data)
            file.close()
            # Schedule cron
            os.system('crontab -l > jobs.cron')
            jobs_file = open('jobs.cron', 'a')
            jobs_file.write('*/' + job_json[0]['interval'] + ' * * * * python ' + config.root_dir + "/process_job.py " + config.root_dir + "/" + job_filename + "\n")
            jobs_file.close()
            os.system('crontab ' + config.root_dir + '/jobs.cron')
            os.system('rm jobs.cron')
            return True
        except:
            return False

if __name__ == "__main__":
    HOST, PORT = "localhost", config.port
    server = SocketServer.TCPServer((HOST, PORT), TCPHandler)
    try:
        server.serve_forever()
    except:
        print "Shutting down..."
