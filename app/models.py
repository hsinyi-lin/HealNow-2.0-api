from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, CHAR, Column, Date, DateTime, Float, ForeignKey, Integer, Numeric, String, Table, Text, text
from sqlalchemy.orm import relationship

from .utils import get_tw_time

db = SQLAlchemy()


class Clarification(db.Model):
    __tablename__ = 'clarification'

    id = Column(Integer, primary_key=True, server_default=text("nextval('clarification_id_seq'::regclass)"))
    title = Column(String)
    content = Column(Text)
    url = Column(Text)
    publish_date = Column(Date)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class Med(db.Model):
    __tablename__ = 'med'

    id = Column(Integer, primary_key=True, server_default=text("nextval('med_id_seq'::regclass)"))
    permit_num = Column(String)
    permit_type = Column(String)
    med_tw_name = Column(String)
    med_en_name = Column(String)
    med_type = Column(String)
    composition = Column(String)
    indications = Column(String)
    how_to_use = Column(String)
    permit_date = Column(Date)
    edit_date = Column(Date)
    expiration_date = Column(Date)
    manufacturer = Column(String)
    manufacturer_country = Column(String)
    applicant_name = Column(String)
    applicant_address = Column(String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class News(db.Model):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, server_default=text("nextval('news_id_seq'::regclass)"))
    title = Column(String)
    content = Column(Text)
    url = Column(Text)
    publish_date = Column(Date)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class Pharmacy(db.Model):
    __tablename__ = 'pharmacy'

    id = Column(Integer, primary_key=True, server_default=text("nextval('pharmacy_id_seq1'::regclass)"))
    gender = Column(String)
    pharmacy_name = Column(String)
    phone = Column(String)
    leader_name = Column(String)
    city = Column(String)
    town = Column(String)
    street = Column(String)
    full_address = Column(String)
    latitude = Column(Numeric)
    longitude = Column(Numeric)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(db.Model):
    __tablename__ = 'user'

    email = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)
    gender = Column(CHAR(1), nullable=False)
    photo = Column(Text, nullable=True)
    created_time = Column(DateTime, nullable=False, default=get_tw_time())
    updated_time = Column(DateTime, nullable=False, default=get_tw_time())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Verification(db.Model):
    __tablename__ = 'verification'

    id = Column(Integer, primary_key=True, server_default=text("nextval('verification_id_seq'::regclass)"))
    email = Column(String, nullable=False)
    code = Column(String, nullable=False)
    created_time = Column(DateTime, nullable=False, default=get_tw_time())


class Mood(db.Model):
    __tablename__ = 'mood'

    id = Column(Integer, primary_key=True, server_default=text("nextval('mood_id_seq'::regclass)"))
    email = Column(ForeignKey('user.email'), nullable=False)
    content = Column(String, nullable=False)
    ai_reply = Column(String, nullable=False)
    positive = Column(Numeric)
    neutral = Column(Numeric)
    negative = Column(Numeric)
    sentiment = Column(Integer)
    created_time = Column(DateTime, nullable=False, default=get_tw_time())

    user = relationship('User')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Post(db.Model):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, server_default=text("nextval('post_id_seq'::regclass)"))
    email = Column(ForeignKey('user.email'), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_time = Column(DateTime, nullable=False, default=get_tw_time())
    updated_time = Column(DateTime, nullable=False, default=get_tw_time())

    user = relationship('User')

    def as_dict(self):
        post_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        post_dict['username'] = self.user.username
        return post_dict


class SavedClarification(db.Model):
    __tablename__ = 'saved_clarification'

    id = Column(Integer, nullable=False, server_default=text("nextval('saved_clarification_id_seq'::regclass)"))
    clarification_id = Column(ForeignKey('clarification.id'), primary_key=True, nullable=False)
    email = Column(ForeignKey('user.email'), primary_key=True, nullable=False)

    clarification = relationship('Clarification')
    user = relationship('User')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SavedMed(db.Model):
    __tablename__ = 'saved_med'

    id = Column(Integer, nullable=False, server_default=text("nextval('saved_med_id_seq'::regclass)"))
    med_id = Column(ForeignKey('med.id'), primary_key=True, nullable=False)
    email = Column(ForeignKey('user.email'), primary_key=True, nullable=False)

    user = relationship('User')
    med = relationship('Med')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SavedNew(db.Model):
    __tablename__ = 'saved_news'

    id = Column(Integer, nullable=False, server_default=text("nextval('saved_news_id_seq'::regclass)"))
    news_id = Column(ForeignKey('news.id'), primary_key=True, nullable=False)
    email = Column(ForeignKey('user.email'), primary_key=True, nullable=False)

    user = relationship('User')
    news = relationship('News')


    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Like(db.Model):
    __tablename__ = 'like'

    id = Column(Integer, nullable=False, server_default=text("nextval('like_id_seq'::regclass)"))
    post_id = Column(ForeignKey('post.id'), primary_key=True, nullable=False)
    email = Column(ForeignKey('user.email'), primary_key=True, nullable=False)

    user = relationship('User')
    post = relationship('Post')


class SavedPost(db.Model):
    __tablename__ = 'saved_post'

    id = Column(Integer, nullable=False, server_default=text("nextval('saved_post_id_seq'::regclass)"))
    post_id = Column(ForeignKey('post.id'), primary_key=True, nullable=False)
    email = Column(ForeignKey('user.email'), primary_key=True, nullable=False)

    user = relationship('User')
    post = relationship('Post')


class Comment(db.Model):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, server_default=text("nextval('newtable_id_seq'::regclass)"))
    post_id = Column(ForeignKey('post.id'), nullable=False)
    email = Column(ForeignKey('user.email'), nullable=False)
    content = Column(String, nullable=False)
    created_time = Column(DateTime, nullable=False, default=get_tw_time())
    updated_time = Column(DateTime, nullable=False, default=get_tw_time())

    user = relationship('User')
    post = relationship('Post')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

