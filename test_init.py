import ee
ee.Authenticate()
ee.Initialize(project='gee-wcma-ndvi')
s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
img = s2.first()
print(img.getInfo())
