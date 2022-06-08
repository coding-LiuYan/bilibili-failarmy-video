import json
import re
import urllib3
import requests


urllib3.disable_warnings()


def from_count_page_url_get_bv(url: str, number: int = 100) -> list:
    """
    this function can get all bv number as a list from compilation
    :param url: compilation's link example:https://space.bilibili.com/29440965/channel/collectiondetail?sid=107573
    :param number: videos count, default = 100
    :return: return bv number list
    """

    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "origin": "https://www.bilibili.com",
    }

    # 确定好了爬取的ajax
    re_list = re.findall("\\d+", url)
    url = []
    bv_list = []
    for i in range(int(number/100)+1):
        url.append(f"https://api.bilibili.com/x/polymer/space/seasons_archives_list?mid={re_list[0]}&season_id={re_list[1]}&sort_reverse=false&page_num={i+1}&page_size=100")

    # 爬取ajax里面的BV号
    for i in url:
        res = requests.get(i, headers=head)
        res_json = json.loads(res.text)
        for j in res_json['data']['archives']:
            bv_list.append(j['bvid'])
    return bv_list
