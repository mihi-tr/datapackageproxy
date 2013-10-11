A proxy for DataPackages
========================

DataPackageProxy?
-----------------

[DataPackages](http://data.okfn.org/standards/data-package) are a nice and
neat tool to work with and bundle Data. However, working with them in
browser-based apps is not straight forward. People's hosting doesn't
support [CORS](http://enable-cors.org) so including datapackag files using
e.g. d3.csv does not work :/. *Datapackageproxy* to the rescue!

DatapackageProxy is a appengine based script, that takes a datapackage url
(without the trailing /datapackage.json) and allows you to access it's
resources.

e.g:

```
http://datapackageproxy.appspot.com/resources?n=0&url=http://data.okfn.org/data/bond-yields-uk-10y
```

shows the first resource in the datapackage. If you're not sure which
resource to use, try:

```
http://datapackageproxy.appspot.com/metadata?url=http://data.okfn.org/data/bond-yields-uk-10y
```

This will return the metadata for the package.

Builds on the [datapackage python module](http://github.com/tryggvib/datapackage)
