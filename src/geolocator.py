'''
Created Aug 30, 2013
Major portions of this code were borrowed from a Udacity course
Web Development taught by Steve Huffman of Reddit and Hipmunk
and David Evans of the University of Virginia. 

The code below is a simplified and altered version of an 
asignment in Web Development and is designed to demonstrate
a google map of the user's location. 

IT DOES NOT USE RIGOROUS
ERROR CHECKING AS REQUIRED in a PRODUCION REQUIREMENT
as is with no warranty whatsoever!

@author: Mike Rehner
'''
import urllib2
from xml.dom import minidom
import webapp2

MSG_GEOAPI = "<p> The API that queries your ip address from your browser and returns the latitude and longitude in xml format <a href='http://ip-api.com/xml/' target = '_blank'>http://ip-api.com/xml/</a> </p>"
MSG_MAP = "<p> The Google MAP API is at <a href='https://developers.google.com/maps/documentation/imageapis/' target ='_blank'> https://developers.google.com/maps/documentation/imageapis/</a></p>"
MSG_SOURCE = "<p> This python source code is at <a href='https://github.com/babarehner/GAE-GeoLocator' target='_blank'>https/github.com/babarehner/GAE-GeoLocator</a></p>"

#the html for a web page
index_html = """
    <html>
        <head>
            <title>Simple GeoLocator Page</title>
        </head>
        <body>
            <form method = "post">
                <br />
                What is your name, please?
                <input type = "text" name = "user" maxlength ="12" />
                <br />
                <input type = "submit" />
            </form>
        </body>
    </html>
"""



# returns latitude and longitude from the api_url
def get_latlon(loc_ip):
    #returns an xml file 
    api_url = 'http://ip-api.com/xml/'
    #use loc_ip below for GAE local because localhost 127.0.0.1 will not show a latitude and longitude
    #comment out loc_ip when pushing the code to GAE Cloud (external Google App Engine
    loc_ip = '76.181.140.45' #Use this line for GAW
    try:
        xml = urllib2.urlopen(api_url + loc_ip).read()
    except urllib2.URLError, e:
        return "Unable to get geolocater service " + e.code
    
    if xml:
        pxml = minidom.parseString(xml)
        if pxml:
            p1 = pxml.getElementsByTagName('lat')
            lat = p1[0].childNodes[0].nodeValue
            p2 = pxml.getElementsByTagName('lon')
            lon =  p2[0].childNodes[0].nodeValue
            return lat,lon
        else:
            lat,lon = '0','0'
        return lat,lon
    return 0,0

# returns a google map
def gmaps_img(latd, longt):
    #streetview api "http://maps.googleapis.com/maps/api/streetview?size=200x200&location=40.720032,%20-73.988354&heading=235&sensor=false">
    maps_api ='http://maps.googleapis.com/maps/api/staticmap?size=420x300&sensor=false&' # minimal google map api
    #pts = ''.join('markers=%s,%s' % (latd, longt)) if using markers
    pts = ''.join('center=%s,%s&zoom=11' % (latd, longt))
    return maps_api + pts   

    
class MainPage(webapp2.RequestHandler): 
    # writes out the web page listed above
    def get(self):
        self.response.out.write(index_html)
        
    # writes out the user response to the form
    def post(self):
        username = self.request.get('user')[0:11]
        self.response.out.write('Greetings <strong>' + username + '</strong><br /> Do you want to play hide and seek?')
        
        p1, p2 = get_latlon(self.request.remote_addr) #get the latitude and longitude using the browser remote address 
        self.response.out.write("<p><img src= " + gmaps_img(p1,p2) + " /></p>")
        self.response.out.write(MSG_GEOAPI + MSG_SOURCE + MSG_SOURCE)
           

app = webapp2.WSGIApplication([('/', MainPage)], debug = True)