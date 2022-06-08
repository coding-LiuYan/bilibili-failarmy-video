import json
import re
import time
import requests
import urllib3
import threading
urllib3.disable_warnings()

cookie_head = {}


# 设置cookie头请求
def set_cookie_head(cookie: str):
    if cookie == "" and cookie_head.get('cookie') is not None:
        cookie_head.pop('cookie')
    cookie_head['cookie'] = cookie

    print("目前的cookie头")
    print(cookie_head)


# 代替结构体存储视频所有信息
class VideoInfo:
    def __init__(self, name, size, bv_id, cid_number, video_url, head):
        self.head = head
        self.video_url = video_url
        self.cid_number = cid_number
        self.bv_id = bv_id
        self.size = size
        self.name = name


def get_video_info(share_url: str) -> VideoInfo:
    """
    can get the video all information
    :param share_url: video url example
    :return: VideoInfo class include many~ many~ base info
    """
    # 提取分享链接中的BV号
    # share_url: str = input("input share link:")
    start: int = share_url.find("BV")

    bv_id = share_url[start: start+12]

    # print(bv_id)

    # 获得cid号
    bv_url = f"https://api.bilibili.com/x/player/pagelist?bvid={bv_id}&jsonp=jsonp"
    response = requests.get(bv_url)
    url_json = json.loads(response.text)
    # print(url_json)
    cid_number: int = url_json['data'][0]['cid']
    # 获得视频名字
    name = url_json['data'][0]['part']

    # 获得视频流地址

    last_url = f"https://api.bilibili.com/x/player/playurl?cid={cid_number}&bvid={bv_id}&qn=116&type=&otype=json"
    # print(last_url)
    response = requests.get(last_url, headers=cookie_head)
    url_json = json.loads(response.text)
    video_url = url_json['data']['durl'][0]['url']
    # print(url_json)
    # 获得视频大小
    size = url_json['data']['durl'][0]['size']

    # 生成访问这个视频流的请求头
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "origin": "https://www.bilibili.com",
    }
    flv_host = re.compile("https://(.*)(com|cn)", re.I)
    # print(video_url)
    host_str = flv_host.search(video_url).group()
    head['authority'] = host_str[9:]
    head["referer"] = share_url

    return VideoInfo(name, size, bv_id, cid_number, video_url, head)


def download_video(video_info: VideoInfo):
    """
    can change the info to a video in local
    :param video_info: like name, need a whole info class
    :return: in your cp will have a video
    """
    res = requests.get(video_info.video_url, headers=video_info.head, stream=True, verify=False)
    with open("./output/{name}.flv".format(name=video_info.name), "wb") as f:
        for i in res.iter_content(2048):
            f.write(i)


def download_videos(bv_list: list, sleep_time: int = 5):
    """
    what the fxxk thing
    :param bv_list: bv list like ['BV xxx', 'BV xxx', ....]
    :param sleep_time: wait for thread download, don't be too arrogant, default 5s
    :return: download videos in local pc
    """
    thread_list = []
    number = 1
    for i in bv_list:
        tmp = get_video_info(f"https://www.bilibili.com/video/{i}")
        tmp.name = f"{number}. {tmp.name}"
        print(tmp.name + " 加入下载线程...下载中")
        number += 1
        tmp_thread = threading.Thread(target=download_video, args=(tmp,))
        tmp_thread.start()
        thread_list.append(tmp_thread)
        time.sleep(sleep_time)

    print("downloading...")
    for i in thread_list:
        i.join()
    print("completed!!!")
