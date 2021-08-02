# Muallif: Otaboboyev Akmal
# http://t.me/Python_uzbek

import requests
from bs4 import BeautifulSoup
import json
import os 
def siteurl(name, k=1):
    path = os.getcwd()+"/datas/"
    if os.path.exists(path)==False:
        os.mkdir(path)
    with open(f"{path}{name}.json", "w", encoding="utf-8") as file:
        datas = []
        for page in range(1,k+1):
            url = f"http://uzmovi.com/{name}/page/{page}"
            resp = requests.get(url)
            src = BeautifulSoup(resp.text, "lxml")
            div = src.find("div", {"id":"dle-content"}).find_all("div", class_="short-content")
            a_link = [ [x.find("a").get("href"), x.find("a").get("title")] for x in div]
            for x in a_link:
                datas.append(get_data(x[0]))
            print(f"[+] {page} of {k}")
        print("[+] All resources downloaded")
        json.dump(datas,file,indent=4,ensure_ascii=False)
        print("[+] All resources saved")

def get_data(url=""):
    resp = requests.get(url)
    src = BeautifulSoup(resp.text, "lxml")
    # print(resp.text)
    div = src.find_all("div", class_="col-sm-8 col-xs-12") # col-sm-8 col-xs-12
    div_title = div[0].find_all("div","finfo-title")
    div_text = div[0].find_all("div","finfo-text")
    x = [x.text for x in div_title]
    y = [y.text for y in div_text]
    data = {
        "url":url
        }
    for a in range(len(x)):
        data[x[a]] = y[a]
    return data


def number_pages(name):
    url = f"http://uzmovi.com/{name}"
    resp = requests.get(url)
    src = BeautifulSoup(resp.text, "lxml")
    a = src.find("div", class_="pages-numbers").find_all("a")
    return int(a[-1].text)
    

def main():
    names = [
            "multfilm", # 0
            "tarjima-kinolar", # 1 
            "serial", # 2
            "uzbek-kinolar", # 3
            "hind-kinolar" # 4
            ]
    for name in names:
        print(f"[+] Run {name=}")
        k = number_pages(name)
        siteurl(name, k)
        print("[+]","="*20,"[+]")
    

if __name__=="__main__":
    main()
