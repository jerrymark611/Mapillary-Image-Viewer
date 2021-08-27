# %%
import os
import mercantile, mapbox_vector_tile, requests, json
from vt2geojson.tools import vt_bytes_to_geojson


# %%
# define an empty geojson as output
# def query(west: float, south: float, east: float, north, access_token: str):
# # define an empty geojson as output
# output = {"type": "FeatureCollection", "features": []}
#
# # vector tile endpoints -- change this in the API request to reference the correct endpoint
# tile_coverage = 'mly1_public'
#
# # tile layer depends which vector tile endpoints:
# # 1. if map features or traffic signs, it will be "point" always
# # 2. if looking for coverage, it will be "image" for points, "sequence" for lines, or "overview" for far zoom
# tile_layer = "image"
#
# # Mapillary access token -- user should provide their own
#
# # west, south, east, north = [-80.12823442840576, 25.77376933762778, -80.1264238357544, 25.788608487732198]
#
# # get the list of tiles with x and y coordinates which intersect our bounding box
# # MUST be at zoom level 14 where the data is available, other zooms currently not supported
#
# # loop through list of tiles to get tile z/x/y to plug in to Mapillary endpoints and make request
# tiles = list(mercantile.tiles(west, south, east, north, 14))
# seq_count = 0
# img_count = 0
# # loop through list of tiles to get tile z/x/y to plug in to Mapillary endpoints and make request
# for tile in tiles:
#     tile_url = 'https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}'.format(tile_coverage, tile.z,
#                                                                                            tile.x, tile.y,
#                                                                                            access_token)
#     response = requests.get(tile_url)
#     data = vt_bytes_to_geojson(response.content, tile.x, tile.y, tile.z, layer=tile_layer)
#
#     # push to output geojson object if yes
#     for feature in data['features']:
#
#         # get lng,lat of each feature
#         lng = feature['geometry']['coordinates'][0]
#         lat = feature['geometry']['coordinates'][1]
#
#         # ensure feature falls inside bounding box since tiles can extend beyond
#         if west < lng < east and south < lat < north:
#
#             # create a folder for each unique sequence ID to group images by sequence
#             sequence_id = feature['properties']['sequence_id']
#             if not os.path.exists(os.path.join('data', sequence_id)):
#                 os.makedirs(os.path.join('data', sequence_id))
#                 seq_count += 1
#
#             # request the URL of each image
#             image_id = feature['properties']['id']
#             request_image(access_token, sequence_id, image_id)

# return f"{img_count} images of {seq_count} sequence have been downloaded"
# return request_sequence(access_token, 'Vg5L4tS6eWFcGMlUY9xyB3')

def query(access_token, sequence_id):
    return request_sequence(access_token, sequence_id)


def request_sequence(access_token, sequence_id):
    header = {'Authorization': 'OAuth {}'.format(access_token)}
    url = 'https://graph.mapillary.com/image_ids?sequence_id={}'.format(sequence_id)
    r = requests.get(url, headers=header)
    data = r.json()
    # print(data['data'])
    if not os.path.exists(os.path.join('data', sequence_id)):
        os.makedirs(os.path.join('data', sequence_id))
    for value in data['data']:
        request_image(access_token, sequence_id, value['id'])
    return


def request_image(access_token, sequence_id, image_id):
    header = {'Authorization': 'OAuth {}'.format(access_token)}
    url = 'https://graph.mapillary.com/{}?fields=thumb_2048_url'.format(image_id)
    r = requests.get(url, headers=header)
    data = r.json()
    image_url = data['thumb_2048_url']
    # save each image with ID as filename to directory by sequence ID
    if os.path.isfile('{}/{}.jpg'.format(sequence_id, image_id)):
        return

    with open('data/{}/{}.jpg'.format(sequence_id, image_id), 'wb') as handler:
        image_data = requests.get(image_url, stream=True).content
        handler.write(image_data)
    return
