from configure import config
from function import check
from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
from function.SpsParser import Sps21Parser
from sqlalchemy.orm import sessionmaker
from db.dbtable import X
from sqlalchemy import and_



class DbLoad(QRunnable):
    def __init__(self, engine, data_file: str):
        super().__init__()
        self.engine = engine
        self.data_file = data_file

        self.signals = WorkerSignal()

    @pyqtSlot()
    def run(self):
        self.signals.start.emit(False)
        line_numbers = check.iter_count(self.data_file)
        self.signals.process_max.emit(line_numbers)
        table_name = choose_table(self.data_file)
        parser = Sps21Parser()
        #        print(line_numbers)
        counter = 0
        with self.engine.connect() as con:
            #con.execute("PRAGMA synchronous=OFF")  # 关闭同步
            #con.execute("BEGIN TRANSACTION")  # 显式开启事务
            try:
                with open(self.data_file) as fr:
                    for line in fr:
                        parsed = parser.parse_point(line)
                        if parsed:
                            counter += 1
                            db_point_update(con,table_name,parsed)
                            if counter % 100000 == 0:
                                self.signals.process.emit(counter)
                                print(counter)
                                #con.commit()
                        #con.commit()
            except Exception as e:
                print(str(e))
        self.signals.process.emit(counter)
        self.signals.finished.emit(True)


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


def db_point_update(conn, DB_TABLE, sps_data):
    line = sps_data[1]
    point = sps_data[2]
    idx = sps_data[3]
    easting = sps_data[10]
    northing = sps_data[11]
    elevation = sps_data[12]
    if elevation == None:
        elevation = 0
    c = conn  #.cursor()
    sql_insert = "INSERT OR REPLACE INTO " + DB_TABLE + " (line, point, idx, x, y, z) VALUES (?, ?, ?, ?, ?, ?);"
    data = (line, point, idx, easting, northing, elevation)
    c.execute(sql_insert, data)
    # print(sql_insert, data)
    # conn.commit()
    c.close()


def get_record_for_point(conn, DB_TABLE, key_list: list):
    """
    :param conn:
    :param key_list:
    :return:
    """
    c = conn.cursor()
    c.execute("SELECT * FROM " + DB_TABLE + " WHERE line =? and point = ? and idx = ?",
              (key_list[0], key_list[1], key_list[2]))
    rows = c.fetchall()
    if len(rows) > 0:
        data = rows[0]  # [rows[0][0], rows[0][1], rows[0][2], rows[0][3], rows[0][4], rows[0][5]]
        return data


def clear(conn, DB_TABLE):
    # conn = self.create_connection(db_file)
    c = conn.cursor()
    sql = "DELETE from " + DB_TABLE
    c.execute(sql)
    conn.commit()
    conn.close()


class WorkerSignal(QObject):
    start = pyqtSignal(bool)
    process = pyqtSignal(int)
    process_max = pyqtSignal(int)
    finished = pyqtSignal(bool)
