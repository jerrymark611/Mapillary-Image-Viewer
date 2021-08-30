# %%
import mercantile, requests
from vt2geojson.tools import vt_bytes_to_geojson
from math import sin, cos, asin, sqrt, radians, degrees, atan2
import json
# %%
# get metadata inside an area
def query_area(access_token: str, west: float, south: float, east: float, north: float):
    tile_coverage = 'mly1_public'
    tile_layer = "image"
    output= { "type": "FeatureCollection", "features": [] } 


    # west, south, east, north = 120.43976795391002, 23.525173201509304, 120.4875756473915, 23.5965857805608
    tiles = list(mercantile.tiles(west, south, east, north, 14))
    

    # loop through list of tiles to get tile z/x/y to plug in to Mapillary endpoints and make request
    for i, tile in enumerate(tiles):
        print(f"{i}/{len(tiles)}")
        tile_url = 'https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}'.format(tile_coverage,tile.z,tile.x,tile.y,access_token)
        response = requests.get(tile_url)
        data = vt_bytes_to_geojson(response.content, tile.x, tile.y, tile.z,layer=tile_layer)
        

        for feature in data['features']:
            if feature['properties']['is_pano']:
                output['features'].append(feature)
    with open('images.geojson', 'w') as f:
        json.dump(output, f)
    return output

# distance between two points
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * asin(sqrt(a)) * 1000

def getDegree(lon1, lat1, lon2, lat2):  
    radLatA = radians(lat1)  
    radLonA = radians(lon1)  
    radLatB = radians(lat2)  
    radLonB = radians(lon2)  
    dLon = radLonB - radLonA  
    y = sin(dLon) * cos(radLatB)  
    x = cos(radLatA) * sin(radLatB) - sin(radLatA) * cos(radLatB) * cos(dLon)  
    brng = degrees(atan2(y, x))  
    brng = (brng + 360) % 360  
    return brng  


def find_closest_point(access_token: str, lon, lat):
    tile_coverage = 'mly1_public'
    tile_layer = "image"
    output= { "type": "FeatureCollection", "features": [] } 


    west, south, east, north = lon-1e-14, lat-1e-14, lon+1e-14, lat+1e-14
    tiles = list(mercantile.tiles(west, south, east, north, 14))
    
    # loop through list of tiles to get tile z/x/y to plug in to Mapillary endpoints and make request
    for i, tile in enumerate(tiles):
        tile_url = 'https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}'.format(tile_coverage,tile.z,tile.x,tile.y,access_token)
        response = requests.get(tile_url)
        data = vt_bytes_to_geojson(response.content, tile.x, tile.y, tile.z,layer=tile_layer)
        

        for feature in data['features']:
            lon2, lat2 = feature['geometry']['coordinates']
            distance = haversine(lon, lat, lon2, lat2)
            # get panoramic images of distance less than 50 meters
            if distance < 100 and  feature['properties']['is_pano']:
                image_url = request_image(access_token,  feature['properties']['id'])
                feature['img_url'] = image_url
                feature['degree'] = getDegree(lon, lat, lon2, lat2)
                output['features'].append(feature)
    with open('data/images.geojson', 'w') as f:
        json.dump(output, f)
    
    return output

def request_image(access_token, image_id):
    header = {'Authorization': 'OAuth {}'.format(access_token)}
    url = 'https://graph.mapillary.com/{}?fields=thumb_2048_url'.format(image_id)
    r = requests.get(url, headers=header)
    data = r.json()
    return data['thumb_2048_url']
    
