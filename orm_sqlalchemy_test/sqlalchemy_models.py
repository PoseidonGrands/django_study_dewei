# from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base


# 配置连接
engine = create_engine('mysql+pymysql://root:2280139492@localhost:3306/sqlalchemy_test')
# 作为所有模型，使用基类可以自动地从 Python 类生成数据库表，以及从数据库表生成对应的 Python 类
Base = declarative_base()
# 用于CRUD
db_session = sessionmaker(bind=engine)


def init():
    Base.metadata.create_all(engine)


def drop():
    Base.metadata.drop_all()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))


if __name__ == '__main__':
    init()
    user = User(name='lisi')
    # 增加用户
    session = db_session()
    session.add(user)
    session.commit()
    session.close()

    # 查询用户
    session = db_session()
    # 获得的是一个集合
    user = session.query(User).filter_by(name='zhangsan')
    print(list(user)[0].name)
