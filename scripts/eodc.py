
import os
import json
import openeo
from openeo.rest.imagecollectionclient import ImageCollectionClient


def eodc_script(output_filename):
    """
    
    """
    
    backend_url = 'https://openeo.eodc.eu'

    session = openeo.connect(backend_url, auth_type='basic', auth_options={"username": os.environ["EODC_USERNAME"], "password": os.environ["EODC_PASSWORD"]})
    minx = 11.279182434082033
    maxx = 11.406898498535158
    maxy = 46.522729291844286
    miny = 46.464349400461145
    epsg = "EPSG:4326"
    spatial_extent = {'west':minx,'east':maxx,'north':maxy,'south':miny,'crs':epsg}

    temporal_extent=["2018-06-04T00:00:00.000Z","2018-06-23T00:00:00.000Z"]

    spectral_extent = [8, 4, 2]

    s2a = ImageCollectionClient.load_collection(
                        session=session,
                        collection_id='s2a_prd_msil1c',
                        temporal_extent=temporal_extent,
                        spatial_extent=spatial_extent,
                        bands=spectral_extent
                        )        
    s2b = s2a.load_collection(
                        session=session,
                        collection_id='s2b_prd_msil1c',
                        temporal_extent=temporal_extent,
                        spatial_extent=spatial_extent,
                        bands=spectral_extent
                        )
    s2_radiometry = s2a.merge(s2b)
    
    #s2_radiometry = 
    B02 = s2_radiometry.band(2)
    B04 = s2_radiometry.band(1)
    B08 = s2_radiometry.band(0)

    evi_cube = (2.5 * (B08 - B04)) / ((B08 + 6.0 * B04 - 7.5 * B02) + 10000)

    min_evi = evi_cube.min_time()

    output = min_evi.download(output_filename,format="GTiff")
