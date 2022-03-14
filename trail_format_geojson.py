import json
import os
from tqdm import tqdm

if __name__ == '__main__':
    init_path = '../data/trails_init/'
    result_path = '../data/trails_geojson/'
    all_files = os.listdir(init_path)
    exist_file = os.listdir(result_path)
    p_bar = tqdm(total=len(all_files))
    for file in all_files:
        if file in exist_file:
            p_bar.update(1)
            continue
        try:
            json_data = json.loads(open(init_path + file, mode='r', encoding='utf-8').read())
            coord_text = json_data['coords']
            coord_text = coord_text[2:]
            coord_text = coord_text[0:-2]
            coord_text = coord_text.split('], [')

            coords = []
            timestamps = []
            alts = []
            speeds = []
            miles = []
            for text in coord_text:
                te = text.split(',')
                r = [te[0][1:-1], float(te[1]), float(te[2]), float(te[3]), float(te[4]), float(te[5])]
                timestamps.append(r[0])
                coords.append([r[2], r[1]])
                alts.append(r[3])
                speeds.append(r[4])
                miles.append(r[5])

            result_geojson = {
                "type": "FeatureCollection",
                "name": "traveler tracks",
                "crs": {
                    "type": "name",
                    "properties": {
                        "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                    }
                },
                "features": [
                    {
                        "type": "Feature",
                        "properties": {
                            "timestamp": timestamps,
                            "alt": alts,
                            "speed": speeds,
                            "miles": miles,
                            "id": json_data['id'],
                            "time": json_data['time']
                        },
                        "geometry": {
                            "type": "MultiLineString",
                            "coordinates": [
                                coords
                            ]
                        }
                    }]
            }
            file_name = file.split('.')[0]
            open(result_path + file_name+'.geojson', mode='a+', encoding='utf-8').write(
                json.dumps(result_geojson, indent=4, ensure_ascii=False))
            p_bar.update(1)
        except Exception as e:
            print('')
            print(file)
            print(e)
            p_bar.update(1)
            # print(e)
