# Python 3 server example
import matplotlib.pyplot as plt
import numpy as np
import sympy
import time
import base64
import urllib.parse as urlparse

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
from io import BytesIO
from urllib.parse import parse_qs
from sympy import *

name=""


hostName = "localhost"
serverPort = 8090

 
 
#A lancer avec http://127.0.0.1:8090/ depuis firefox p/ex

class MyServer(BaseHTTPRequestHandler):
 
    def do_GET(self):
 
        v=2000
        vx=100
        g=9.8
        m=10
        h=0
 
        # récupération de paramètres de l'url
        query_string = self.path.split("?")
        if len(query_string)>1:
            print(query_string[1])
            params = query_string[1].split("&")
            if len(params)>3:
                p1 =params[0].split("=")
                v  =float(p1[1])
                p2 =params[1].split("=")
                vx =float(p2[1])
                p3 =params[2].split("=")
                m  =float(p3[1])
                p4 =params[3].split("=")
                h  =float(p4[1])
 
                    
        # résolution symbolique avec sympy -> echelle ordonnee (0 de la trajectoire)
        x    = symbols('x')
        eq   = Eq(h + v*x - 0.5*m*g*x*x)
        sol  = solve((eq),(x))
        maxt = sol[1]
        step = maxt/100
        maxx = (maxt+step)*vx
 
        # url avec /garph dedans = génère l'image png avec mathplot
        if self.path.find("graph1")>0:
 
            # plot équation temps
            t = np.arange(0.0, maxt+step, step)
            s = h + v*t - 0.5*g*t*t
            fig, ax = plt.subplots()
            ax.set_title('Trajectoire selon t[s],y[m]')
            ax.plot(t, s)
           
            # récupère le graphe en binaire pour le retour d'image http
            stream = BytesIO()
            plt.savefig(stream, format='png')
            stream.seek(0)  # rewind to beginning of file
           
            self.send_response(200)
            self.send_header('Content-type','image/png')
            self.end_headers()
            self.wfile.write(stream.getvalue())
           
        elif self.path.find("graph2")>0:

            # plot équation x,y
            t = np.arange(0,maxt+step, step)
            x, y = vx*t, h + v*t - 0.5*g*t*t
            fig, ax = plt.subplots()
            ax.set_title('Trajectoire selon x [m],y[m]')
            ax.plot(x, y)
           
            # récupère le graphe en binaire pour le retour d'image http
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
            self.wfile.write(bytes("<form action=go><body>", "utf-8"))
            self.wfile.write(bytes("<h1>Simulation balistique</h1><p>Vitesse verticale et horizontale : <br><input name=v value='"+str(v)+"'> <input name=vx value='"+str(vx)+"'></p><p>Masse : <br><input name=m value='"+str(m)+"'></p><p>Hauteur: <br><input name=h value='"+str(h)+"'></p><input  type=submit value=OK></p>", "utf-8"))
            self.wfile.write(bytes('<img src="/graph1?v='+str(v)+'&vx='+str(vx)+'&m='+str(m)+'&h='+str(h)+'"></img>' , "utf-8"))
            self.wfile.write(bytes('<img src="/graph2?v='+str(v)+'&vx='+str(vx)+'&m='+str(m)+'&h='+str(h)+'"></img>' , "utf-8"))
            self.wfile.write(bytes("</body></form></html>", "utf-8"))

           
 
if name == "__main__":      
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
    
