# !/usr/bin/env python
# coding: utf-8
import os
import requests
import json
import urllib
from trans import decode
import socket
import threading
import Queue

count = 1
queue = Queue.Queue()
socket.setdefaulttimeout(10)

header = {
    'Host': "image.baidu.com",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
}

url = 'https://image.baidu.com/search/acjson'


class ImgThread(threading.Thread):
    def __init__(self, func):
        super(ImgThread, self).__init__()
        self.func = func

    def run(self):
        self.func()


def worker():
    while not queue.empty():
        url = queue.get()
        save(url)
        queue.task_done()


def save(url_save):
    global count

    target = save_path + '\\%s.jpg' % count
    try:
        global sums
        sums = count
        urllib.urlretrieve(url_save, target)
        count += 1
    except Exception:
        pass


def get_url(word, num):
    url_list = set()
    for j in range(1, num + 1):

        send_data = {
            "queryWord": word,
            "tn": "resultjson_com",
            "ipn": "rj",
            "word": word,
            "qc": "",
            "nc": 1,
            "fr": "",
            "pn": 30 * j,
            "rn": 30,
        }

        content = requests.get(url, headers=header, params=send_data)
        data = json.loads(content.content)["data"]
        for i in range(len(data) - 1):
            objurl = data[i]['objURL']
            imgurl = decode(objurl)
            url_list.add(imgurl)

    return url_list


def get_img(word, page_num, thread_num=30, path=None, delete_file_size=10240):
    global sums
    global save_path

    if path is None:
        if not os.path.exists(os.path.join(os.getcwd(), 'img')):
            os.mkdir(os.path.join(os.getcwd(), 'img'))
        save_path = os.path.join(os.getcwd(), 'img')
    else:
        if not os.path.exists(path):
            raise ValueError("the directory: %s does not exist, please check again" % path)
        save_path = path

    urls = get_url(word, page_num)
    for url in urls:
        queue.put(url)

    threads = []
    for i in range(thread_num):
        t = ImgThread(worker)
        t.setDaemon(True)
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()
    queue.join()

    num = 1
    for n in range(1, int(sums) + 1):
        try:
            if os.path.getsize(save_path + '\\%s.jpg' % n) < delete_file_size:
                os.remove(save_path + '\\%s.jpg' % n)
                num += 1
        except Exception:
            num += 1

    print 'done %s' % (int(sums) - num + 1)


if __name__ == '__main__':
    get_img("外国美女", 2)
