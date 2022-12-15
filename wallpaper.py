import json
import time
import os
import threading

import requests
from bs4 import BeautifulSoup
import ctypes
import tempfile

class Manager:
    def __init__(self):
        self.save_path = "C:/Users/Zeal/Desktop/"
        self.rankings = self.getSoup("https://www.pixiv.net/ranking.php").find_all("section", attrs={"data-id": True})
        self.pids = [item["data-id"] for item in self.rankings]
        self.titles = [item["data-title"] for item in self.rankings]
        self.artists = [item["data-user-name"] for item in self.rankings]

    def get_save_path(self):
        return self.save_path
    
    def set_save_path(self, path):
        self.save_path = path
        
    def getInfo(self):
        return (self.pids, self.titles, self.artists)

    def changeWallpaper(self, pic):
        # 使用 tempfile 模块的 NamedTemporaryFile 函数创建一个临时文件
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(pic)
            toDelete = f.name
            ctypes.windll.user32.SystemParametersInfoW(20, 0, f.name, 0)
        # 等待壁纸切换完成后删除临时文件
        time.sleep(5)
        os.remove(toDelete)

    def newThreadTask(self, func, myArgs):
        threading.Thread(target=func, args=myArgs).start()

    def getSoup(self, url):
        try:
            res = requests.get(url, timeout=5)
        except requests.exceptions.Timeout:
            print("Timeout")
            return None
        return BeautifulSoup(res.text, "html.parser")

    def getPicsByPid(self, pid):
        pics = {}
        url = f'https://www.pixiv.net/ajax/illust/{pid}/pages?lang=zh'
        try:
            response = requests.get(url, timeout=5).text
        except requests.exceptions.Timeout:
            print("Timeout")
            return None
        res_json = json.loads(response)

        for datas in res_json['body']:
            download_url = datas['urls']['original']
            try:
                response = requests.get(download_url, timeout=5, headers={
                    "referer": f"https://www.pixiv.net/artworks/{pid}",
                })
            except requests.exceptions.Timeout:
                print("Timeout")
                return None
            pics[download_url.split('/')[-1]] = response.content
            time.sleep(1)

        return pics
    
    def savePic(self, pic_name, content):
        with open(f"{self.save_path}{pic_name}", 'wb') as f:
            f.write(content)
        


    # for pid, title, artist in zip(pids, titles, artists):
    #     print(f"Downloading {title} by {artist}")
    #     pics = getPicsByPid(pid)
    #     for pic_name, pic in pics.items():
    #         with open(f"{SAVE_PATH}{pic_name}", 'wb') as f:
    #             f.write(pic)
    


if __name__ == "__main__":
    manager = Manager()

    pids, titles, artists = manager.getInfo()
    
    print(f"id: {pids[0]}; {titles[0]} by {artists[0]}")
    manager.newThreadTask(manager.changeWallpaper, (manager.getPicsByPid(pids[0])[list(manager.getPicsByPid(pids[0]).keys())[0]],))
    
    manager.savePic(list(manager.getPicsByPid(pids[0]).keys())[0], manager.getPicsByPid(pids[0])[list(manager.getPicsByPid(pids[0]).keys())[0]])
        














