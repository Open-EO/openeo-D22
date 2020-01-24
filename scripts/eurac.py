
import os
import json
import openeo
from openeo.rest.imagecollectionclient import ImageCollectionClient


def eurac_script(input_data, output_filename):
    """
    
    """
    

    backend_url = 'https://openeo.eurac.edu'
    
    if input_data == 'L1C':
        collection_id = 'openEO_S2_32632_10m_L1C_D22'
    elif input_data == 'L2A':
        collection_id = 'openEO_S2_32632_10m_L2A_D22'

    session = openeo.connect(backend_url, auth_type='basic', auth_options={"username": os.environ["EURAC_USERNAME"], "password": os.environ["EURAC_PASSWORD"]})

    minx = 11.279182434082033
    maxx = 11.406898498535158
    maxy = 46.522729291844286
    miny = 46.464349400461145
    epsg = "EPSG:4326"

    s2_radiometry = ImageCollectionClient.load_collection(
                        session=session,
                        collection_id=collection_id,
                        temporal_extent=["2018-06-04T00:00:00.000Z","2018-06-23T00:00:00.000Z"],
                        spatial_extent={'west':minx,'east':maxx,'north':maxy,'south':miny,'crs':epsg},
                        bands=["B08", "B04", "B02"]
                        )                    
    B02 = s2_radiometry.band(2)
    B04 = s2_radiometry.band(1)
    B08 = s2_radiometry.band(0)

    evi_cube = (2.5 * (B08 - B04)) / ((B08 + 6.0 * B04 - 7.5 * B02) + 10000)

    min_evi = evi_cube.min_time()
    
    output = min_evi.download(output_filename,format="GTiff")
