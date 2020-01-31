
import os
import json
import openeo
from openeo.rest.imagecollectionclient import ImageCollectionClient


def mundialis_script(output_filename):
    """
    
    """
    

    backend_url = 'https://openeo.mundialis.de'
    
    collection_id = 'utm32n.openeo_bolzano.strds.openeo_bolzano_S2'

    session = openeo.connect(backend_url, auth_type='basic', auth_options={"username": os.environ["MUNDIALIS_USERNAME"], "password": os.environ["MUNDIALIS_PASSWORD"]})

    minx = 10.44662475585937
    maxx = 10.62927246093749
    maxy = 46.84516443029275
    miny = 46.72574176193996
    epsg = "EPSG:4326"

    s2_radiometry = ImageCollectionClient.load_collection(
                        session=session,
                        collection_id=collection_id,
                        temporal_extent=["2018-05-01T00:00:00.000Z","2018-10-01T00:00:00.000Z"],
                        spatial_extent={'west':minx,'east':maxx,'north':maxy,'south':miny,'crs':epsg}
                        )                    
    B02 = s2_radiometry.band("S2_2")
    B04 = s2_radiometry.band("S2_4")
    B08 = s2_radiometry.band("S2_8")

    evi_cube = (2.5 * (B08 - B04)) / ((B08 + 6.0 * B04 - 7.5 * B02) + 10000)

    min_evi = evi_cube.min_time()
    
    output = min_evi.download(output_filename,format="GTiff")

