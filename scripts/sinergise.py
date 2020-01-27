import json
import openeo
from openeo.rest.imagecollectionclient import ImageCollectionClient


def sinergise_script(output_filename):
    """
    
    """

    backend_url = 'https://e3oind87n9.execute-api.eu-central-1.amazonaws.com/production/'
    #'https://openeo.sentinel-hub.com/production'
    collection_id = 'S2L1C'

    session = openeo.connect(backend_url)

    minx = 11.279182434082033
    maxx = 11.406898498535158
    maxy = 46.522729291844286
    miny = 46.464349400461145
    epsg = "EPSG:4326"
    spatial_extent = {'west':minx,'east':maxx,'north':maxy,'south':miny,'crs':epsg}

    temporal_extent=["2018-06-04T00:00:00.000Z","2018-06-23T00:00:00.000Z"]

    spectral_extent = ["B08", "B04", "B02"]

    s2_radiometry = ImageCollectionClient.load_collection(
                        session=session,
                        collection_id=collection_id,
                        temporal_extent=temporal_extent,
                        spatial_extent=spatial_extent
                        )

    B02 = s2_radiometry.band(spectral_extent[2])
    B04 = s2_radiometry.band(spectral_extent[1])
    B08 = s2_radiometry.band(spectral_extent[0])

    evi_cube = (2.5 * (B08 - B04)) / ((B08 + 6.0 * B04 - 7.5 * B02) + 1.0)

    min_evi = evi_cube.min_time()

    min_evi.download(output_filename, format="GTiff", options={"datatype": "float32"})
