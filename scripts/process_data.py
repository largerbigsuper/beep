import json
import os


FILE_PATH = os.path.join(os.path.dirname(__file__), 'data/area.json')
# SAVE_PATH = os.path.join(os.path.dirname(__file__), 'data/area_provine_city.json')
SAVE_PATH = os.path.join(os.path.dirname(__file__), 'data/area_provine_city_district.json')

def run():
    print('begin ...')
    with open(FILE_PATH) as f:
        area_json = json.loads(f.read())
        for province in area_json:
            province_name = province['name']
            province_code = province['code']
            city_list = province['children']
            for city in city_list:
                city_name = city['name']
                city_code = city['code']
                district_list = city['children']
                for district in district_list:
                    district_name = district['name']
                    district_code = district['code']
                    del district['children']
            print(province_name + 'done')
        with open(SAVE_PATH, 'w') as save_file:
            save_file.write(json.dumps(area_json, ensure_ascii=False))
    print('end')