from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, Float, Boolean, Date
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:1@localhost/postgres", echo=False)
session = scoped_session(sessionmaker())
session.configure(bind=engine, autoflush=False, expire_on_commit=False)

Base = declarative_base()


class Order(Base):
    """ Таблица с заказами """
    __tablename__ = "order"
    id = Column(Integer(), primary_key=True)
    order_number = Column(String())
    price_dollar = Column(Float())
    date = Column(Date())
    price_rubles = Column(String())


class SubscribedUser(Base):
    """ Таблица с пользователями, подписавшимися на уведомления в Телеграм """
    __tablename__ = "subscribed_users"
    id = Column(String(), primary_key=True)
    username = Column(String())


# при запуске таблицы пересоздаются - этого можно и не делать, но в ТЗ ничего про это не говорится
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
