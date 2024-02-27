import requests
import json
import time
from bs4 import BeautifulSoup

root_url = 'https://www.gequbao.com/'


def main():
    # read song name from file
    with open('songs.txt', 'r') as f:
        songs = f.readlines()
        for song in songs:
            try:
                download(song.split('.mp3')[0].strip())
                time.sleep(1)
            except Exception as e:
                print('下载失败:', song.split('.mp3')[0].strip())
                with open('failed.txt', 'a') as f:
                    f.write(song.split('.mp3')[0].strip() + '\n')
                continue


def download(song):
    print('正在下载:', song)
    html = requests.get(root_url + 's/' + song).text
    soup = BeautifulSoup(html, 'html.parser')
    first_link = soup.find('a', href=True, string='下载')
    if first_link:
        href_value = first_link['href']
        # print('目录:', href_value)
        # print(href_value.split('/')[2])
        referer = root_url + 's/' + href_value
        song_url = requests.get(
            root_url + '/api/play_url?id=' + href_value.split('/')[2] + '&json=1')
        mp3_url = json.loads(song_url.text)['data']['url']
        song_file = requests.get(mp3_url, headers={'Referer': referer})
        # write to /run/media/xxx/xxx
        with open('/run/media/xun/disk/' +
                  song + '.mp3', 'wb') as f:
            f.write(song_file.content)
        print('下载完成:', song)
    else:
        print('未找到符合条件的链接')


if __name__ == '__main__':
    main()
