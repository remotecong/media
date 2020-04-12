import requests
import pydash
import os
import json
from bs4 import BeautifulSoup
import re

WOL_HOST = "https://wol.jw.org"
WOL_MEETINGS_URL = "/en/wol/dt/r1/lp-e"
SETTINGS_PATH = ".settings.json"

def get_url(url):
    with requests.get(f"{WOL_HOST}{url}", headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0",
        }) as r:
        return r

def download_meeting_catolog():
    return parse_meeting_catalog(get_url(WOL_MEETINGS_URL).text)

def parse_meeting_catalog(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select(".groupTOC a")
    return get_watchtower_images(links[0]["href"])

def get_watchtower_images(url):
    if url:
            soup = BeautifulSoup(get_url(url).text, 'html.parser')
            images = []
            for img in soup.select("#article figure img"):
                data = {"src": img["src"]}
                q = img.parent.find("figcaption")
                if q:
                    data["paragraphs"] = pydash.get(re.search(r"see\sparagraphs?\s([\d-]+)", q.text.strip(), flags=re.IGNORECASE), '1')
                images.append(data)
            save_watchtower_images(images)
            return images

def save_watchtower_images(images):
    save_path = get_save_path()
    for img in images:
        name = os.path.basename(img["src"])
        if "paragraphs" in img:
            name += f" para_{img['paragraphs']}"
        with requests.get(f"{WOL_HOST}{img['src']}", stream=True) as r:
            path = os.path.join(save_path, f"{name}.jpg")
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=128):
                    f.write(chunk)
        print(f"SAVED {name}")



def get_save_path():
    if not os.path.isfile(SETTINGS_PATH):
        return request_save_path()

    try:
        with open(SETTINGS_PATH) as f:
            save_path = pydash.get(json.load(f), 'savePath')
            if os.path.isdir(save_path):
                return save_path
            else:
                return request_save_path()
    except:
        return request_save_path()


def request_save_path():
    needs_path = True

    while needs_path:

        path = input("Enter a path to save files: ")
        needs_path = not os.path.isdir(path)
        if (needs_path):
            print(f"Couldn't find '{path}'. Why don't you try again?")

    with open(SETTINGS_PATH, 'w') as f:
        if not path.endswith('/'):
            path = path + '/'

        json.dump({'savePath': path}, f)

    return path


if __name__ == '__main__':
    import sys

    download_meeting_catolog()
    print("Goodbye")

