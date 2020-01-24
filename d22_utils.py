import numpy as np
from osgeo import osr

import json

import matplotlib.pyplot as plt
from mpl_toolkits import axes_grid1


def get_query_bbox(json_file):
    
    geodata0 = json.load(open(json_file))
    geodata = geodata0['features'][0]['geometry']['coordinates'][0]
    
    minx = geodata[0][0]
    maxx = geodata[1][0]
    miny = geodata[0][1]
    maxy = geodata[2][1]
    query_bbox = [[minx, minx, maxx, maxx, minx], [miny, maxy, maxy, miny, miny]]
    
    return query_bbox

def add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
    """Add a vertical color bar to an image plot."""
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1./aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    
    cbar = im.axes.figure.colorbar(im, cax=cax, **kwargs)
    cbar.set_label('minimum EVI', rotation=270)
    

def print_info(data):
    print('Raster shape:', data.shape)
    print('Min:', round(np.nanmin(data), 3))
    print('Mean:', round(np.nanmean(data), 3))
    print('Median:', round(np.nanmedian(data), 3))
    print('Max:', round(np.nanmax(data), 3))
    print('Negative values [%]:', np.round(np.sum(data < 0) / (data.shape[0] * data.shape[1]), decimals=3) * 100, '%')
    print('Negative values (<-1000) [%]:', np.round(np.sum(data < -1000) / (data.shape[0] * data.shape[1]), decimals=3) * 100, '%')
    print('Zero values [%]:', np.round(np.sum(data == 0) / (data.shape[0] * data.shape[1]), decimals=3) * 100, '%')
    print('Nan values [%]:', np.round(np.sum(np.isnan(data)) / (data.shape[0] * data.shape[1]), decimals=3) * 100, '%')
    print('\n')
    

def get_extent(ds, geographic=False):
      """
      Returns the extent of the raster as (xmin, ymin, xmax, ymax)
      Output is in raster projection by default, or in geographic if flagged.

      Example(s):
          get_extent()
          get_extent(geographic=True)

      Parameters
      ----------
      geographic (default, False): bool

      Returns
      -------
      4-element tuple (xmin, ymin, xmax, ymax)

      """
      
      size_raster = [ds.RasterXSize, ds.RasterYSize]

      pix_x = np.array((0, size_raster[0]))
      pix_y = np.array((0, size_raster[1]))
      geotransform = ds.GetGeoTransform()
      x_coords = geotransform[0] + \
                (pix_x * geotransform[1]) + \
                (pix_y * geotransform[2])
      y_coords = geotransform[3] + \
                (pix_x * geotransform[4]) + \
                (pix_y * geotransform[5])

      if geographic:
          src_srs = osr.SpatialReference(wkt=ds.GetProjection())
          trg_srs = osr.SpatialReference()
          trg_srs.ImportFromEPSG(4326)
          transform = osr.CoordinateTransformation(src_srs, trg_srs)
          transformed_x = []
          transformed_y = []
          for k, _ in enumerate(x_coords):
              x_trans, y_trans, _ = transform.TransformPoint(x_coords[k], y_coords[k])
              transformed_x.append(x_trans)
              transformed_y.append(y_trans)
          x_coords, y_coords = (transformed_x, transformed_y)

      xmin = min(x_coords[0], x_coords[1])
      xmax = max(x_coords[0], x_coords[1])
      ymin = min(y_coords[0], y_coords[1])
      ymax = max(y_coords[0], y_coords[1])
      
      #raster_extent = [xmin, ymin, xmax, ymax]
      raster_extent = [xmin, ymin, xmax, ymax]
      raster_extent = [xmin, xmax, ymin, ymax]
      #minx, maxx, miny, maxy = raster_extent[0], raster_extent[1], raster_extent[2], raster_extent[3]
      raster_bbox = [[xmin, xmin, xmax, xmax, xmin], [ymin, ymax, ymax, ymin, ymin]]
      
      return raster_extent, raster_bbox
      
      
