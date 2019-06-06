from bottle import run, get
from bs4 import BeautifulSoup
import requests
import json
# from pytube import YouTube
import pafy
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound


baza = create_engine('sqlite:///youtube.sqlite3')
BazaModel = declarative_base()
Session = sessionmaker(bind=baza)


def findByUrl(url):
    try:
        session = Session()
        youtube = session.query(Youtube).filter_by(url='{0}'.format(url)).one()
        session.close()
        return youtube
    except NoResultFound:
        return None


def createUrl(url):
    session = Session()
    session.add(Youtube(url=url))
    session.commit()
    session.close()


def addTitle(url, title):
    conn = baza.connect()
    stmt = update(Youtube).values(title=title).where(Youtube.url == url)
    conn.execute(stmt)
    conn.close()


def addViews(url, views):
    conn = baza.connect()
    stmt = update(Youtube).values(views=views).where(Youtube.url == url)
    conn.execute(stmt)
    conn.close()


def addDesc(url, description):
    conn = baza.connect()
    stmt = update(Youtube).values(description=description).where(Youtube.url == url)
    conn.execute(stmt)
    conn.close()


def addAuthor(url, author):
    conn = baza.connect()
    stmt = update(Youtube).values(author=author).where(Youtube.url == url)
    conn.execute(stmt)
    conn.close()


def addAuthorImg(url, author_img):
    conn = baza.connect()
    stmt = update(Youtube).values(author_img=author_img).where(Youtube.url == url)
    conn.execute(stmt)
    conn.close()


def addCoverImg(url, cover_img):
    conn = baza.connect()
    stmt = update(Youtube).values(cover_img=cover_img).where(Youtube.url == url)
    conn.execute(stmt)
    conn.close()


class Youtube(BazaModel):
    __tablename__ = 'youtube'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    title = Column(String)
    views = Column(String)
    description = Column(String)
    author = Column(String)
    author_img = Column(String)
    cover_img = Column(String)


Session = sessionmaker(bind=baza)


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
    youtube = findByUrl(url)
    if youtube:
        if youtube.views is not None:
            return youtube.views
        else:
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
            addViews(url, text_to_parse.split(":")[1].replace('\"', ""))
            return view_count
    else:
        createUrl(url)
        getViews(url)


@get('/desc/<url>')
def getDescription(url):
    youtube = findByUrl(url)
    if youtube:
        if youtube.description is not None:
            return youtube.description
        else:
            video = pafy.new(url)
            addDesc(url, video.description)
            return video.description
    else:
        createUrl(url)
        getDescription(url)


@get('/title/<url>')
def getTitle(url):
    youtube = findByUrl(url)
    if youtube:
        if youtube.title is not None:
            return youtube.title
        else:
            video = pafy.new(url)
            addTitle(url, video.title)
            return video.title
    else:
        createUrl(url)
        getTitle(url)


@get('/cover/<url>')
def getCover(url):
    youtube = findByUrl(url)
    if youtube:
        if youtube.cover_img is not None:
            return youtube.cover_img
        else:
            cover = "https://img.youtube.com/vi/" + url + "/maxresdefault.jpg"
            addCoverImg(url, "<img src=" + cover + " alt=\"Cover\">")
            return "<img src=" + cover + " alt=\"Cover\">"
    else:
        createUrl(url)
        getCover(url)

@get('/author/<url>')
def getAuthor(url):
    youtube = findByUrl(url)
    if youtube:
        if youtube.author is not None:
            return youtube.author
        else:
            video = pafy.new(url)
            addAuthor(url, video.author)
            return video.author
    else:
        createUrl(url)
        getAuthor(url)


@get('/author-img/<url>')
def getAuthorImg(url):
    youtube = findByUrl(url)
    if youtube:
        if youtube.author_img is not None:
            return youtube.author_img
        else:
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

            addAuthorImg(url, """<img """ + div1[index] + """ alt="Author">""")
            return """<img """ + div1[index] + """ alt="Author">"""
    else:
        createUrl(url)
        getAuthorImg(url)


run(reloader=True, debug=True)
