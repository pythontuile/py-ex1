 # Python 3 server example
import matplotlib.pyplot as plt
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from os import curdir, sep
import base64
from io import BytesIO
 
hostName = "localhost"
serverPort = 8090

#A lancer avec http://127.0.0.1:8090/ depuis firefox p/ex

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
 
        if self.path=="/graph":
            plt.plot([1, 2, 3, 4])
            plt.ylabel('some numbers')
            
            stream = BytesIO()
            plt.savefig(stream, format='png')
            stream.seek(0)  # rewind to beginning of file
            
            self.send_response(200)
            self.send_header('Content-type','image/png')
            self.end_headers()
            self.wfile.write(stream.getvalue())
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>Entrer la fonction <input name=fct> <input  type=submit value=GO></p>", "utf-8"))
            self.wfile.write(bytes('<img src="/graph"></img>' , "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
 
           
 
if __name__ == "__main__":       
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
 
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
 
    webServer.server_close()
    print("Server stopped.")
 
