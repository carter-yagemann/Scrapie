import BaseHTTPServer
import SocketServer
import os
import json

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Scrapie</title></head>")
        s.wfile.write("<body>")
        if s.path.find(".csv") == -1:
            files = os.listdir("data")
            for file in files:
                s.wfile.write("<p><a href='data/" + file + "'>" + file + "</a></p>")
        else:
            file = open(s.path[1:], "r")
            job  = open(s.path[1:].replace("data", "jobs").replace("csv", "job"), "r")
            s.wfile.write("<h2>" + json.loads(job.read())[0]['url'] + "</h2>")
            for row in file:
                s.wfile.write("<p>" + row + "</p>")
            file.close()
            job.close()
        s.wfile.write("</body></html>")

PORT = 8000

Handler = MyHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
