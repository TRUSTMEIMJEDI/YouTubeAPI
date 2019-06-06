import os
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

# if os.path.exists('youtube.db'):
#     os.remove('youtube.db')
# tworzymy instancję klasy Engine do obsługi bazy
baza = create_engine('sqlite:///youtube.sqlite3')  # ':memory:'

# klasa bazowa
BazaModel = declarative_base()


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


# tworzymy tabele
# BazaModel.metadata.create_all(baza)


Session = sessionmaker(bind=baza)
# session = Session()
# session.add(Youtube(url='w0WJ8limSR8',
#                     title='''Pretty Lights - One Day They'll Know (ODESZA Remix)''',
#                     views='9954',
#                     description='',
#                     author='Chill Nation',
#                     author_img='',
#                     cover_img=''))
# session.commit()

# session.add(Youtube(url='w0WJ8limSR8',
#                     title='''Pretty Lights - One Day They'll Know (ODESZA Remix)''',
#                     views='9954'))
# session.commit()


def findByUrl(url):
    try:
        session = Session()
        #    youtube = session.query(Youtube).filter_by(url=url).one()
        youtube = session.query(Youtube).filter(Youtube.url == url).one()
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


# createUrl('w0WJ8limSR8')
# addTitle('w0WJ8limSR8', 'test')
yt = findByUrl('w0WJ8limSR8')
print(yt.title)

