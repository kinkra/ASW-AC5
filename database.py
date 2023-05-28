from flask import request
import sqlalchemy as sql
from sqlalchemy.orm import DeclarativeBase, Session

engine = sql.create_engine('mssql+pyodbc://DB-AWS:coxinha123@PEDRO')
sess = Session(engine)
conn = engine.connect()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    id = sql.Column('id', sql.Integer, primary_key=True, autoincrement=True)
    name = sql.Column('name', sql.String(50), nullable=False)
    email = sql.Column('email', sql.String(100), nullable=False, unique=True)
    password = sql.Column('password', sql.String, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f'ID: {self.id}, Name: {self.name}, Email: {self.email}'


class Todo(Base):
    __tablename__ = 'todo'
    id = sql.Column('id', sql.Integer, primary_key=True, autoincrement=True)
    desc = sql.Column('desc', sql.String, nullable=False)
    user_id = sql.Column('user_id', sql.Integer,
                         sql.ForeignKey("user.id"), nullable=False)

    def __init__(self, desc, user_id):
        self.user_id = user_id
        self.desc = desc

    def __repr__(self) -> str:
        return f'ID: {self.id}, User ID: {self.user_id}'


# -------------------------------------------------------------------------------
def checkmail(email):
    with sess:
        return True if sess.query(User).filter(User.email == email).first() else False


def checklogin(email, password):
    with sess:
        return True if sess.query(User).filter(
            sql.and_(
                User.email == email,
                User.password == password
            )
        ).first() else False


def check_id(session):
    email = session[request.cookies.get('id_sessao')]
    with sess:
        return (sess.query(User).filter(User.email == email).first()).id


def add_user(nome, email, senha):
    with sess:
        sess.add(User(nome, email, senha))
        sess.commit()


def make_todo(text, user_id):
    with sess:
        sess.add(Todo(text, user_id))
        sess.commit()


def todo_list(id_usuario):
    list = []
    with sess:
        for text in sess.query(Todo).filter(Todo.user_id == id_usuario):
            list.append(text.desc)
    return list