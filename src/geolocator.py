'''
Created Aug 30, 2013

@author: Mike Rehner
'''
import urllib2
from xml.dom import minidom
import webapp2

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
    api_url = 'http://ip-api.com/xml/'
    #loc_ip = '76.181.140.45'
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


def gmaps_img(latd, longt):
    # streetview api "http://maps.googleapis.com/maps/api/streetview?size=200x200&location=40.720032,%20-73.988354&heading=235&sensor=false">

    maps_api ='http://maps.googleapis.com/maps/api/staticmap?size=420x300&sensor=false&' # minimal google api
    #pts = ''.join('markers=%s,%s' % (latd, longt))
    pts = ''.join('center=%s,%s&zoom=11' % (latd, longt))
    return maps_api + pts   

    
class MainPage(webapp2.RequestHandler): 
    def get(self):
        self.response.out.write(index_html)
        
    def post(self):
        msg_api = "<p> The Google MAP API is at <a href='https://developers.google.com/maps/documentation/imageapis/' target ='_blank'> https://developers.google.com/maps/documentation/imageapis/</a></p>"
        msg_sourcecode = "<p> The python source code is at <a href='https://github.com/babarehner/GAE-GeoLocator' target='_blank'>https/github.com/babarehner/GAE-GeoLocator</a></p>"
        username = self.request.get('user')[0:11]
        self.response.out.write('Greetings <strong>' + username + '</strong><br /> Do you want to play hide and seek?')
        
        p1, p2 = get_latlon(self.request.remote_addr)
        self.response.out.write("<p><img src= " + gmaps_img(p1,p2) + " /></p>")
        self.response.out.write(msg_api + msg_sourcecode)
           

app = webapp2.WSGIApplication([('/', MainPage)], debug = True)