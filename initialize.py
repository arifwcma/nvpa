import ee
service_account = 'gee-service@gee-wcma-ndvi.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, 'keys/gee-wcma-ndvi-d4bccc119cbf.json')
ee.Initialize(credentials)
print("Initialized")
