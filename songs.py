import requests
import pydash
import os
import json

MEETING_SONGS_JSON_URL = "https://data.jw-api.org/mediator/v1/categories/E/VODSJJMeetings?detailed=1&clientType=www"
SETTINGS_PATH = ".settings.json"

def get_manifest():
    with requests.get(MEETING_SONGS_JSON_URL) as r:
        return pydash.get(r.json(), 'category.media')


def get_song_url(medias, song_num):
    # songs are ordered in array
    # files stored in quality ASC order
    # 720p is last (currently 4th index)
    return pydash.get(medias, f"{song_num - 1}.files.3.progressiveDownloadURL")


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


def save_song(manifest, song_num, save_path):
    url = get_song_url(manifest, song_num)
    if url:
        print(f"SAVING: Song {song_num}")
        path = os.path.join(save_path, f"Song {song_num:03}.mp4")
        with requests.get(url, stream=True) as r:
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=128):
                    f.write(chunk)
        print(f"SAVED: Song {song_num}")
    else:
        print(f"Failed to find 720p version for song {song_num}")


if __name__ == '__main__':
    import sys

    save_location = get_save_path()
    medias = get_manifest()

    if len(sys.argv) > 1:
        songs = [int(x) for x in sys.argv[1:]]
        for s in songs:
            save_song(medias, s, save_location)
        print("Goodbye")
    else:
        print(f"There are {len(medias)} songs available")

