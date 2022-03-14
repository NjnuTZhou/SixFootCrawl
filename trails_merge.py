import json
import os
from tqdm import tqdm

init_file_path = '../data/trails_extracted/'

all_files = os.listdir(init_file_path)
result_file = {
    "type": "FeatureCollection",
    "name": "traveler tracks",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    },
    "features": []
}

p_bar = tqdm(total=len(all_files))
for file in all_files:
    geojson = json.loads(open(init_file_path+file,mode='r',encoding='utf-8').read())
    result_file["features"].append({
        "type": "Feature",
        "properties": {
            'id':geojson['features'][0]["properties"]["id"]
        },
        "geometry":geojson['features'][0]['geometry']
    })
    p_bar.update(1)

open('traveler_trails.geojson',mode='a+',encoding='utf-8').write(json.dumps(result_file,indent=4,ensure_ascii=False))