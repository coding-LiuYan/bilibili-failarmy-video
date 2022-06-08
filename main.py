from get_count import *
from download_video import *


"""
本入口运行可以输入合集链接进行一个视频滴下载！ 视频存放在output中
"""
if __name__ == '__main__':
    input_url = input("请输入合集链接：")
    input_number = input("视频数量超过一百个请输入视频数量（没有直接回车）：")
    input_time = input("下载视频的间隔（回车默认5s），不怕封IP打个0!：")
    input_cookie = input("输入你b站登录用的cookie（回车默认无 最高画质只有720p）(输入过了不用输入)：")

    if input_number == "":
        input_number = 100

    if input_time == "":
        input_time = 5
    else:
        input_time = int(input_time)

    if input_cookie != "":
        set_cookie_head(input_cookie)
        with open("cookie.txt", "w") as f:
            f.write(input_cookie)
    else:
        with open("cookie.txt", "r") as f:
            set_cookie_head(f.read())

    bv_tmp = from_count_page_url_get_bv(input_url, input_number)
    download_videos(bv_tmp, input_time)
