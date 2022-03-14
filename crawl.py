from bs4 import BeautifulSoup
import requests
import time
import urllib.parse
import json
from tqdm import tqdm
import random
import os


def get_one_trail(tid, t):
    url = 'http://www.foooooot.com/trip/' + tid + '/trackjson/'
    re = requests.get(url)
    try:
        if re.status_code != 200:
            print('request fail')
            return False
        coords = re.text
        if len(coords) == 0:
            # print('request coords is null')
            return True
        open('../data/trails_init/' + tid + '.json', mode='w', encoding='utf-8').write(
            json.dumps({
                "coords": coords,
                "time": t,
                "id": tid
            }, indent=4, ensure_ascii=False))
        return True
    except Exception as e:
        print(e)
        return False


def get_one_page_content(page_index, list_index, exist_files):
    page_url = 'http://www.foooooot.com/search/trip/all/112/all/occurtime/descent/?page='+str(page_index)+'&keyword=%E7%B4%AB%E9%87%91%E5%B1%B1'
    try:
        request = requests.get(page_url)
        if request.status_code != 200:
            return {
                "status": False,
                "list_index": list_index
            }
        html = request.text
        soup = BeautifulSoup(html, 'lxml')
        lis = soup.select('div[class="listSection"] > ul[class="tripsList"] > li')
        page_list_index = list_index
        p_bar = tqdm(total=len(lis) - 2)
        p_bar.update(page_list_index - 1)
        while page_list_index < len(lis) - 1:
            tr = lis[page_list_index].select_one('table > tr')
            td = tr.select_one('td')
            dl = td.select_one('td > div > dl')
            dt = dl.select_one('dt')
            a = dt.select_one('p > a')
            a_href = a.get('href')
            _tid = a_href.split('/')[2]

            if _tid + '.json' in exist_files:
                p_bar.update(1)
                page_list_index += 1
                continue

            dd = dl.select('dd')[1]
            _time = dd.get_text().replace('\n', '').replace(' ', '')
            _time = _time[2:12]
            if get_one_trail(_tid, _time):
                p_bar.update(1)
                page_list_index += 1
                time.sleep(random.randint(2, 6))
            else:
                return {
                    "status": False,
                    "list_index": page_list_index
                }
        return {
            "status": True,
        }

    except Exception as e:
        print(e)
        return {
            "status": False,
            "list_index": list_index
        }


if __name__ == "__main__":
    crawl_condition = json.loads(open('crawl_condition.json', mode='r', encoding='utf-8').read())
    _page_index = crawl_condition['page_index']
    _list_index = crawl_condition['list_index']
    _exist_files = os.listdir('../data/trails_init/')
    while _page_index <= 77:
        print('-----------------------crawling page ' + str(_page_index))
        page_status = get_one_page_content(_page_index, _list_index, _exist_files)
        if not page_status['status']:
            open('crawl_condition.json', mode='w', encoding='utf-8').write(json.dumps({
                "page_index": _page_index,
                "list_index": page_status['list_index']
            }))
            break
        else:
            _page_index += 1
            _list_index = 1
