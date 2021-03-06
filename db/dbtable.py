from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import MetaData
from configure import config

# engine = None

# engine = create_engine("sqlite:///:C:\2020LY\PythonTest\Database ORM\data\001.sqlite", echo=False)
Base = declarative_base()


# Student类相当于在sql中创建的一张表
class Rps(Base):
    __tablename__ = "R"
    line = Column(Float(10.2), primary_key=True)
    point = Column(Float(10.2), primary_key=True)
    idx = Column(Integer, primary_key=True)
    x = Column(Float(10.2))
    y = Column(Float(10.2))
    z = Column(Float(10.2))

    # def __repr__(self):
    #     return "id:%s day:%s name:%s score:%s stu_id:%s" \
    #            %(self.id, self.day, self.name, self.score, self.stu_id)


class Sps(Base):
    __tablename__ = "S"
    line = Column(Float(10.2), primary_key=True)
    point = Column(Float(10.2), primary_key=True)
    idx = Column(Integer, primary_key=True)
    x = Column(Float(10.2))
    y = Column(Float(10.2))
    z = Column(Float(10.2))


class Xps(Base):
    __tablename__ = 'X'
    sline = Column(Float, primary_key=True)
    spoint = Column(Float, primary_key=True)
    sidx = Column(Integer, primary_key=True)
    template_id = Column(Integer)


class Template(Base):
    __tablename__ = 'template'
    id = Column(Integer, primary_key=True)
    sline = Column(Float)
    spoint = Column(Float)
    sidx = Column(Integer)
    from_ch = Column(Integer)
    to_ch = Column(Integer)
    rline = Column(Float)
    from_rp = Column(Float)
    to_rp = Column(Float)
    ridx = Column(Integer)
    temp_id = Column(Integer, ForeignKey("X.template_id"))

    xps = relationship("Xps", backref="point_template")

    def __repr__(self):
        return "id:%d sline:%10.1f spoint:%10.1f sidx:%10.1f from_ch:%10.1f to_ch:%10.1f rline:%10.1f from_rp:%10.1f to_rp:%10.1f ridx:%10.1f temp_id:%10.1f" \
               % (self.id, self.sline, self.spoint, self.sidx, self.from_ch, self.to_ch, self.rline, self.from_rp,
                  self.to_rp, self.ridx, self.temp_id)


# class Template(Base):
#     __tablename__ = 'template'
#     id = Column(Integer, primary_key=True)
#     sline = Column(Float, primary_key=True)
#     spoint = Column(Float)
#     sidx = Column(Integer)
#     relations = relationship("Xps", back_populates='template')
#
#
# class Xps(Base):
#     __tablename__ = 'xps'
#     id = Column(Integer, primary_key=True)
#     sline = Column(Float)
#     spoint = Column(Float)
#     sidx = Column(Integer)
#     from_ch = Column(Integer)
#     to_ch = Column(Integer)
#     rline = Column(Float)
#     from_rp = Column(Float)
#     to_rp = Column(Float)
#     ridx = Column(Integer)
#     template = relationship("Template")
#     template_id = Column(Integer, ForeignKey('template.id'))


def table_create(engine):
    try:
        Base.metadata.create_all(engine, checkfirst=True)
    except Exception as e:
        print(str(e))


def choose_table(data_file):
    with open(data_file) as sps:
        line = sps.readline()
        while line:
            if line[0:1] not in config.table_dict.keys():
                pass
            else:
                break
            line = sps.readline()
    sps.close()
    return line[0:1]


def truncate_db(engine):
    # delete all table data (but keep tables)
    # we do cleanup before test 'cause if previous test errored,
    # DB can contain dust
    meta = MetaData(bind=engine, reflect=True)
    con = engine.connect()
    trans = con.begin()
    #    con.execute('SET FOREIGN_KEY_CHECKS = 0;')
    for table in meta.sorted_tables:
        con.execute(table.delete())
    #    con.execute('SET FOREIGN_KEY_CHECKS = 1;')
    trans.commit()
