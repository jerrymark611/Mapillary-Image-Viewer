# %%
import mercantile, requests
from vt2geojson.tools import vt_bytes_to_geojson
from math import sin, cos, asin, sqrt, radians

# %%
# get metadata inside an area
# def query_area(west: float, south: float, east: float, north: float, access_token: str):
#     # define an empty geojson as output
#     output = {"type": "FeatureCollection", "features": []}

#     # vector tile endpoints -- change this in the API request to reference the correct endpoint
#     tile_coverage = 'mly1_public'

#     # tile layer depends which vector tile endpoints:
#     # 1. if map features or traffic signs, it will be "point" always
#     # 2. if looking for coverage, it will be "image" for points, "sequence" for lines, or "overview" for far zoom
#     tile_layer = "image"

#     # Mapillary access token -- user should provide their own

#     # west, south, east, north = [-80.12823442840576, 25.77376933762778, -80.1264238357544, 25.788608487732198]

#     # get the list of tiles with x and y coordinates which intersect our bounding box
#     # MUST be at zoom level 14 where the data is available, other zooms currently not supported

#     # loop through list of tiles to get tile z/x/y to plug in to Mapillary endpoints and make request
#     tiles = list(mercantile.tiles(west, south, east, north, 14))
#     seq_count = 0
#     img_count = 0
#     # loop through list of tiles to get tile z/x/y to plug in to Mapillary endpoints and make request
#     for tile in tiles:
#         tile_url = 'https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}'.format(tile_coverage, tile.z,
#                                                                                             tile.x, tile.y,
#                                                                                             access_token)
#         response = requests.get(tile_url)
#         data = vt_bytes_to_geojson(response.content, tile.x, tile.y, tile.z, layer=tile_layer)

#         # push to output geojson object if yes
#         for feature in data['features']:

#             # get lng,lat of each feature
#             lng = feature['geometry']['coordinates'][0]
#             lat = feature['geometry']['coordinates'][1]

#             # ensure feature falls inside bounding box since tiles can extend beyond
#             if west < lng < east and south < lat < north:

#                 # create a folder for each unique sequence ID to group images by sequence
#                 sequence_id = feature['properties']['sequence_id']
#                 if not os.path.exists(os.path.join('data', sequence_id)):
#                     os.makedirs(os.path.join('data', sequence_id))
#                     seq_count += 1

#                 # request the URL of each image
#                 image_id = feature['properties']['id']
#                 request_image(access_token, sequence_id, image_id)

#     return f"{img_count} images of {seq_count} sequence have been downloaded"

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * asin(sqrt(a))


def find_closest_point(access_token: str, lon, lat):
    tile_coverage = 'mly1_public'
    tile_layer = "image"


    west, south, east, north = lon-1e-14, lat-1e-14, lon+1e-14, lat+1e-14
    tiles = list(mercantile.tiles(west, south, east, north, 14))
    
    closest_feature = None
    min_distance = float('inf')

    # loop through list of tiles to get tile z/x/y to plug in to Mapillary endpoints and make request
    for i, tile in enumerate(tiles):
        tile_url = 'https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}'.format(tile_coverage,tile.z,tile.x,tile.y,access_token)
        response = requests.get(tile_url)
        data = vt_bytes_to_geojson(response.content, tile.x, tile.y, tile.z,layer=tile_layer)
        
        for feature in data['features']:
            lon2, lat2 = feature['geometry']['coordinates']
            if haversine(lon, lat, lon2, lat2) < min_distance and feature['properties']['is_pano']:
                closest_feature = feature
                
    if closest_feature:
        return request_image(access_token,  closest_feature['properties']['id'])
    else:
        return None





def request_image(access_token, image_id):
    header = {'Authorization': 'OAuth {}'.format(access_token)}
    url = 'https://graph.mapillary.com/{}?fields=thumb_2048_url'.format(image_id)
    r = requests.get(url, headers=header)
    data = r.json()
    return data['thumb_2048_url']
    # save each image with ID as filename to directory by sequence ID
    # if os.path.isfile('{}/{}.jpg'.format(sequence_id, image_id)):
    #     return

    # with open('data/{}/{}.jpg'.format(sequence_id, image_id), 'wb') as handler:
    #     image_data = requests.get(image_url, stream=True).content
    #     handler.write(image_data)
    
