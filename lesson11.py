# Create two points geometry
from osgeo import ogr
wkt_forum = "POINT (51.985306 5.663717)"
wkt_gaia = "POINT (51.987447 5.665508)"
pt_forum = ogr.CreateGeometryFromWkt(wkt_forum)
pt_gaia = ogr.CreateGeometryFromWkt(wkt_gaia)
print(pt_forum)
print(pt_gaia)


# Define spatial reference
## spatial reference
from osgeo import osr
spatialRef = osr.SpatialReference()
spatialRef.ImportFromEPSG(4326)  # from EPSG - Lat/long


# Reproject the points
## lat/long definition
WGS84 = osr.SpatialReference()
WGS84.ImportFromEPSG(4326)

RD_NEW = osr.SpatialReference()
RD_NEW.ImportFromEPSG(28992)

## transform points from WGS84 to RD_NEW
transform = osr.CoordinateTransformation(WGS84, RD_NEW)
point_forum = ogr.CreateGeometryFromWkt(wkt_forum)
point_gaia = ogr.CreateGeometryFromWkt(wkt_gaia)
point_forum.Transform(transform)
point_gaia.Transform(transform)
print point_forum.ExportToWkt()
print point_gaia.ExportToWkt()


# Create shapefiles
## set working directory
import os
os.chdir('/home/user/Geoscripting/PYTHON_WEEK/Lesson1')
print os.getcwd()

## Is the ESRI Shapefile driver available?
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName( driverName )
if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName

## choose name
fn = "WUR.shp"
layername = "wur_buildings"

## Create shape file
ds = drv.CreateDataSource(fn)
print ds.GetRefCount()

# Set spatial reference
spatialReference = osr.SpatialReference()
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

## Create Layer
layer=ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)
print(layer.GetExtent())

forum_building = ogr.Geometry(ogr.wkbPoint)
gaia_building = ogr.Geometry(ogr.wkbPoint)

## SetPoint(self, int point, double x, double y, double z = 0)
forum_building.SetPoint(0,1.0,1.0) 
gaia_building.SetPoint(0,2.0,2.0)

## Export to other formats/representations:
print "KML file export"
print forum_building.ExportToKML()
print gaia_building.ExportToKML()

## Buffering
buffer = gaia_building.Buffer(4,4)
print buffer.Intersects(forum_building)

## Create feature
layerDefinition = layer.GetLayerDefn()
feature_forum = ogr.Feature(layerDefinition)
feature_gaia = ogr.Feature(layerDefinition)

## Add the points to the feature
feature_forum.SetGeometry(forum_building)
feature_gaia.SetGeometry(gaia_building)

## Store the feature in a layer
layer.CreateFeature(feature_forum)
layer.CreateFeature(feature_gaia)
print "The new extent"
print layer.GetExtent()

# export to KML
KML_forum = forum_building.ExportToKML()
KML_gaia = gaia_building.ExportToKML()

ds.Destroy()


