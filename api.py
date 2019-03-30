from bottle import run, get
from bs4 import BeautifulSoup
import requests
import json
from pytube import YouTube
import pafy
# import os


@get('/mp4/<quality>/<url>')
def getMp4(quality, url):
    video = pafy.new(url)
    list_videos = video.allstreams
    for i in range(0, len(list_videos)):
        if list_videos[i].extension == "mp4":
            if list_videos[i].dimensions[1] == 1080:
                index_best = i
            if list_videos[i].dimensions[1] == 720:
                index_high = i
            if list_videos[i].dimensions[1] == 480:
                index_medium = i
            if list_videos[i].dimensions[1] == 360:
                index_low = i

    def quality_of_vid(x):
        switcher = {
            'best': list_videos[index_best],
            'high': list_videos[index_high],
            'medium': list_videos[index_medium],
            'low': list_videos[index_low],
        }
        return switcher.get(x, video.getbestvideo())

    return quality_of_vid(quality).download()


@get('/mp3/<url>')
def getMp3(url):
    video = pafy.new(url)
    audio = video.getbestaudio()
    return audio.download()


@get('/views/<url>')
def getViews(url):
    r = requests.get("https://www.youtube.com/watch?v=" + url)
    web_content = r.text
    soup = BeautifulSoup(web_content, 'lxml')
    views = soup.find_all('script')
    find_view_count = "viewCount"
    for i in range(0, len(views)):
        if find_view_count in views[i].text:
            tab = views[i].text.split(',')
            break

    for i in range(0, len(tab)):
        if find_view_count in tab[i]:
            text_to_parse = (tab[i].replace("\\", ""))
            break

    view_count = json.loads("{" + text_to_parse + "}")
    return view_count


@get('/desc/<url>')
def getDescription(url):
    video = pafy.new(url)
    return video.description


@get('/title/<url>')
def getTitle(url):
    video = pafy.new(url)
    return video.title


@get('/cover/<url>')
def getCover(url):
    cover = "https://img.youtube.com/vi/" + url + "/maxresdefault.jpg"
    return "<img src=" + cover + " alt=\"Cover\">"


@get('/author/<url>')
def getAuthor(url):
    video = pafy.new(url)
    return video.author


@get('/author-img/<url>')
def getAuthorImg(url):
    r = requests.get('https://www.youtube.com/watch?v=' + url)
    web_content = r.content
    soup = BeautifulSoup(web_content, 'html.parser')
    # for i in range(0, 50):
    views = soup.find_all('script')
    text = "window"
    text1 = "viewCount"
    for i in range(0, len(views)):
        if text in views[i].text:
            if text1 in views[i].text:
                tab = views[i].text

    tab1 = tab.replace("\\/", "/")
    tab2 = tab1.replace('\\\"', '"')
    tab3 = tab2.replace("\\\\", "\\")

    tab4 = tab3.split(";")
    for i in range(0, len(tab4)):
        if text1 in tab4[i]:
            tab5 = tab4[i].replace('\\\"', '"')
            tab6 = tab5.replace('""', '"')
            tab7 = tab6.split(",")
            break

    for i in range(0, len(tab7)):
        if "channelId" in tab7[i]:
            channel_id = json.loads("{" + tab7[i] + "}")
            break

    channel = channel_id['channelId']
    r = requests.get('https://www.youtube.com/channel/' + channel)
    web_content = r.content
    soup = BeautifulSoup(web_content, 'html.parser')
    div = soup.find_all('img')
    div1 = str(div[0]).split(" ")
    for i in range(0, len(div1)):
        if "src" in div1[i]:
            index = i
            break

    return """<img """ + div1[index] + """ alt="Author">"""


run(reloader=True, debug=True)
