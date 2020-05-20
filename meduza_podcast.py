import requests
from bs4 import BeautifulSoup
import wget
import os
import time

siteRoot = 'https://meduza.io'


def get_html(url):
    result = requests.get(url)
    return result.text


def get_links(html):
    links = []
    soup = BeautifulSoup(html, 'lxml')
    root = soup.find('ul', {'class': 'Episodes-root'})
    for episode in root.findAll('a', {'class': 'Episodes-download'}):
        link = siteRoot + episode['href']
        links.append(link)
    return links


def DownloadFile(link, path):
    print('\n' + path)
    if os.path.exists(path):
        return
    ok = False
    while not ok:
        try:
            wget.download(link, path)
            ok = True
        except Exception:
            print("Exception")
            time.sleep(2)
            continue


def downloadPodcastEpisodes(folderPath, url):
    links = get_links(get_html(url))
    if not os.path.exists(folderPath):
        os.mkdir(folderPath)
    for link in links:
        path = folderPath + '/' + link.split('/')[-1]
        DownloadFile(link, path)


if __name__ == '__main__':
    downloadPodcastEpisodes('/home/user/Music/Kak_zhit',
                            'https://meduza.io/podcasts/kak-zhit')
    downloadPodcastEpisodes('/home/user/Music/Dva_po_tsene_odnogo',
                            'https://meduza.io/podcasts/dva-po-tsene-odnogo')
    downloadPodcastEpisodes('/home/user/Music/Delo_Sluchaya',
                            'https://meduza.io/podcasts/delo-sluchaya')
