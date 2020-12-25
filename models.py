from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, insert, delete
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError


engine = create_engine('postgresql+psycopg2://postgres:password@localhost/API_DB', client_encoding='utf-8')
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'user_'
    id_user = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String)
    post = relationship('Post', backref='user_')


class Post(Base):
    __tablename__ = 'post'
    id_post = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user_.id_user'))
    header = Column(String)
    text = Column(String)

    def get_dict(self):
        return {
            'id_post': self.id_post,
            'id_user': self.id_user,
            'header': self.header,
            'text': self.text
        }


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    query = insert(User).values([
        {'login': 'Ivan', 'password': '149787a6b7986f31b3dcc0e4e857cd2a'},  # 123450
        {'login': 'Alex', 'password': '5f4dcc3b5aa765d61d8327deb882cf99'},  # password
        {'login': 'Ann', 'password': 'd8578edf8458ce06fbc5bb76a58c5ca4'}    # qwerty
    ])
    try:
        resp = session.execute(query)
        session.commit()
    except IntegrityError:
        print('Error')
