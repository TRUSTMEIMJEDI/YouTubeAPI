import os
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

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
BazaModel.metadata.create_all(baza)
