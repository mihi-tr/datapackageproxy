import csv
import io
import json
import re
import webapp2
from datapackage import DataPackage
from google.appengine.api import urlfetch
from google.appengine.api import memcache

class Resource(webapp2.RequestHandler):
  def get(self):
    url=self.request.get('url',None)
    id=self.request.get('id','')
    if url:
      if not re.match(".*?/$",url):
        url="%s/"%url
      data=memcache.get('resource-%s-%s'%(url,id))
      self.response.headers['Content-Type'] = 'application/CSV; charset=utf-8;'
      self.response.headers['Access-Control-Allow-Origin'] = '*'
      if not data:  
        d=DataPackage("%s"%url)
        try:
          data=[i for i in d.data]
          cols=data[0].keys()
          with io.BytesIO() as sio:
            w=csv.writer(sio)
            w.writerow(cols)
            for i in data:
              w.writerow([i[x] for x in cols])
            memcache.add('resource-%s-%s'%(url,id),sio.getvalue(),300)
            self.response.write(sio.getvalue())
        except ValueError:
          self.response.write("""Decoding of the package failed - this means
          either the resource does not exist - or more likely the data
          contains errors (numbers that are not numbers, dates that cannot
          be parsed etc.)""")
      else:
        self.response.write(data)  
    else:
      self.response.write("Error: please specify URL")
      
    

class MetaData(webapp2.RequestHandler):
  def get(self):
    url=self.request.get('url',None)
    if url:
      if not re.match(".*?/$",url):
        url="%s/"%url
      data=memcache.get('metadata-%s'%url)
      self.response.headers['Content-Type'] = 'application/json; charset=utf-8;'
      self.response.headers['Access-Control-Allow-Origin'] = '*'
      if not data:
        d=DataPackage(url)
        memcache.add('metadata-%s'%url,json.dumps(d.get_descriptor()),300)
        self.response.write(json.dumps(d.get_descriptor()))
      else:
        self.response.write(data)
    else:
      self.response.write("Error: please specify URL")
    

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html; charset=utf-8;'
    with open("index.html") as f:
      self.response.write(f.read())


application=webapp2.WSGIApplication( [
  ('/', MainPage),
  ('/resource', Resource),
  ('/metadata', MetaData),
  ],debug=True)
