"""
    Scrapie Job Upload API Test Data
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

import socket

"""
Test Data
"""
data1 = '[{"url":"https://www.patreon.com/jimquisition", "interval":"60"}, {"element":"totalPatrons", "attribute":"id", "value":"totalPatrons"}, {"element":"span", "attribute":"id", "value":"totalEarnings"}]'

"""
Test method
"""
TCP_IP = '127.0.0.1'
TCP_PORT = 5334
BUFFER_SIZE = 1024
MESSAGE = data1

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print "received data:", data