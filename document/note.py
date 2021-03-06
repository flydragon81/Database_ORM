'''
联合主键（又称复合主键、多重主键）是一个表由多个字段共同构成主键(Primary Key)
'''


from sqlalchemy import Column, String, Integer, and_, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import wdbd.codepool.sqlalchemy.conn as conn

engine = create_engine('sqlite:///%s' % self.from_file)
# 方法1：
class BookOwner(Base):
    # 表的名字:
    __tablename__ = 'book_owner'

    # 表的结构:
    uid = Column('uid', Integer, primary_key=True)
    bid = Column('bid', Integer, primary_key=True)
    name = Column('name', String(20))

    def __repr__(self):
        return "<BookOwner(uid='%s', bid='%s', name='%s')>" % (self.uid, self.bid, self.name)


# 方法2：
class BookOwner(Base):
    # 表的名字:
    __tablename__ = 'book_owner'

    # 表的结构:
    uid = Column('uid', Integer)
    bid = Column('bid', Integer)
    name = Column('name', String(20))

    __table_args__ = (
        PrimaryKeyConstraint('uid', 'bid'),
        {},
    )

    def __repr__(self):
        return "<BookOwner(uid='%s', bid='%s', name='%s')>" % (self.uid, self.bid, self.name)


# 业务处理程序：
class BookManager():

    def __init__(self):
        self.DB_session = sessionmaker(conn.get_conn_engine())

    def create_tables(self):
        # 重建数据库表
        Base.metadata.create_all(conn.get_conn_engine())
        print('重建数据库表结构')

    def add(self, uid, bid, name):
        # 新增对象
        db_session = self.DB_session()
        exsit_obj = db_session.query(BookOwner).filter(and_(BookOwner.uid == uid, BookOwner.bid == bid)).first()
        if exsit_obj:
            print('对象{0}已存在，无法新增！'.format(exsit_obj))
        else:
            bo = BookOwner(uid=uid, bid=bid, name=name)
            db_session.add(bo)
            db_session.commit()
            print('新增完成, {0}'.format(bo))
