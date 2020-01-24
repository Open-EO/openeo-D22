
import os
import json
import openeo
from openeo.rest.imagecollectionclient import ImageCollectionClient

def wwu_gee_script(input_data, output_filename):
    """
    
    """

    backend_url = 'https://earthengine.openeo.org/v0.4'

    if input_data == 'L1C':
        collection_id = 'COPERNICUS/S2'
    elif input_data == 'L2A':
        collection_id = 'COPERNICUS/S2_SR'

    session = openeo.connect(backend_url, auth_type='basic', auth_options={"username": os.environ["WWU_GEE_USERNAME"], "password": os.environ["WWU_GEE_PASSWORD"]})

    minx = 11.279182434082033
    maxx = 11.406898498535158
    maxy = 46.522729291844286
    miny = 46.464349400461145
    epsg = "EPSG:4326"
    spatial_extent = {'west':minx,'east':maxx,'north':maxy,'south':miny,'crs':epsg}

    temporal_extent=["2018-06-04T00:00:00.000Z","2018-06-23T00:00:00.000Z"]

    spectral_extent = ["B8", "B4", "B2"]

    s2_radiometry = ImageCollectionClient.load_collection(
                        session=session,
                        collection_id=collection_id,
                        temporal_extent=temporal_extent,
                        spatial_extent=spatial_extent,
                        bands=spectral_extent
                        )

    B02 = s2_radiometry.band(2)
    B04 = s2_radiometry.band(1)
    B08 = s2_radiometry.band(0)

    evi_cube = (2.5 * (B08 - B04)) / ((B08 + 6.0 * B04 - 7.5 * B02) + 10000)

    min_evi = evi_cube.min_time()

    min_evi_stretched = min_evi.apply(process='linear_scale_range',
                                     data_argument='x', 
                                     arguments={"inputMin": -1, "inputMax": 1, "outputMin": 0, "outputMax": 255}
                                     )
    output = min_evi_stretched.download(output_filename,format="png")
