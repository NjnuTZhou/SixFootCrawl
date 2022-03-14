import json
from osgeo import ogr
import os
from tqdm import tqdm


def if_trail_cross_route(trail, routes):
    for route in routes:
        inter = trail.Intersection(route)
        intersection = json.loads(inter.ExportToJson())
        if intersection['type'] != 'GeometryCollection':
            return True
    return False


if __name__ == '__main__':
    init_path = '../data/trails_geojson/'
    result_path = '../data/trails_extracted/'

    final_count = 0

    init_files = os.listdir(init_path)
    result_files = os.listdir(result_path)
    p_bar = tqdm(total=len(init_files))

    # 读取路网
    route_json = json.loads(open('route.geojson', mode='r', encoding='utf-8').read())
    mxl_routes = []
    for route in route_json["features"]:
        mxl_routes.append(ogr.CreateGeometryFromJson(str(route['geometry'])))
    # print(route_json)

    index = 855
    p_bar.update(index-1)
    while index < len(init_files):
        file = init_files[index]
        if file in result_files:
            index += 1
            p_bar.update(1)
            continue
        geo_json = json.loads(open(init_path + file, mode='r', encoding='utf-8').read())
        geometry = geo_json['features'][0]['geometry']
        if len(geometry['coordinates']) == 0 or len(geometry['coordinates'][0]) < 2:
            index += 1
            p_bar.update(1)
            continue
        feature = ogr.CreateGeometryFromJson(str(geometry))
        if if_trail_cross_route(feature, mxl_routes):
            open(result_path + file, mode='a+', encoding='utf-8').write(
                json.dumps(geo_json, indent=4, ensure_ascii=False))
            final_count += 1
            print(final_count)
        index += 1
        p_bar.update(1)
