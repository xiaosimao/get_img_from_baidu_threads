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
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')
count = 1
queue = Queue.Queue()
socket.setdefaulttimeout(10)
user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0"
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
        url_save, save_path = queue.get()
        save(url_save, save_path)
        queue.task_done()


def save(url_save, save_path):
    global count

    target = save_path + '\\%s.jpg' % count
    try:
        global sums
        sums = count
        urllib.urlretrieve(url_save, target)
        count += 1
    except Exception, e:
        print e
        pass


def reporthook(blocks_read, block_size, total_size):
    has_do = blocks_read * block_size / 1024.0
    to = total_size / 1024.0
    if (has_do / to) > 1:
        print 'down c'


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
        re_url = re.compile(r'"objURL":"(.*?)"')
        content = requests.get(url, headers=header, params=send_data)
        data = [decode(x) for x in re_url.findall(content.content)]
        for i in range(len(data) - 1):
            imgurl = data[i]
            url_list.add(imgurl)

    return url_list


def get_img(word, page_num, thread_num=10, path=None, second_path='img', delete_file_size=10240):
    global sums

    if path is None:
        if not os.path.exists(os.path.join(os.getcwd(), second_path)):
            os.mkdir(os.path.join(os.getcwd(), second_path))
        save_path = os.path.join(os.getcwd(), second_path)
    else:
        if not os.path.exists(path):
            raise ValueError("the directory: %s does not exist, please check again" % path)
        save_path = path

    urls = get_url(word, page_num)
    for url in urls:
        queue.put((url, save_path))

    threads = []
    print "--------start----------"
    for i in range(thread_num):
        t = ImgThread(worker)
        t.setDaemon(True)
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    queue.join()
    print "---------end----------"
    print "-----now,check bad files-----"
    num = 1
    for n in range(1, int(sums) + 1):
        try:
            if os.path.getsize(save_path + '\\%s.jpg' % n) < delete_file_size:
                os.remove(save_path + '\\%s.jpg' % n)
                num += 1
        except Exception:
            num += 1
    print "-----check done-----"
    print 'good file num: %s' % (int(sums) - num + 1)


if __name__ == '__main__':
    get_img("维密", 2)
