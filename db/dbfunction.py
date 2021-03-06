from function import check
from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
from function.SpsParser import Sps21Parser
from sqlalchemy.orm import sessionmaker
from db.dbtable import X
from sqlalchemy import and_


class DbLoad(QRunnable):
    def __init__(self, conn, data_file: str):
        super().__init__()
        self.conn = conn
        self.data_file = data_file

        self.signals = WorkerSignal()

    @pyqtSlot()
    def run(self):
        self.signals.start.emit(False)
        session = sessionmaker(bind=self.conn)
        session = session()

        line_numbers = check.iter_count(self.data_file)
        self.signals.process_max.emit(line_numbers)
        parser = Sps21Parser()
        #        print(line_numbers)
        counter = 0
        try:
            with open(self.data_file) as fr:
                for line in fr:
                    parsed = parser.parse_relation(line)
                    if parsed:
                        counter += 1
                        xx = X(id=counter,
                               line=parsed[5],
                               point=parsed[6],
                               rl=parsed[11],
                               fr=parsed[12],
                               tr=parsed[13])
                        session.add(xx)
                        if counter % 100000 == 0:
                            print(counter)
                            session.commit()
                    session.commit()
        except Exception as e:
            print(str(e))
        self.signals.process.emit(counter)
        self.signals.finished.emit(True)


class DbUpdate(QRunnable):
    def __init__(self, conn, data_file: str):
        super().__init__()
        self.conn = conn
        self.data_file = data_file

        self.signals = WorkerSignal()

    @pyqtSlot()
    def run(self):
        self.signals.start.emit(False)
        session = sessionmaker(bind=self.conn)
        session = session()

        line_numbers = check.iter_count(self.data_file)
        self.signals.process_max.emit(line_numbers)
        parser = Sps21Parser()
        counter = 0
        try:
            with open(self.data_file) as fr:
                for line in fr:
                    parsed = parser.parse_relation(line)
                    if parsed:
                        sx = session.query(X).filter(and_(X.line == parsed[5], X.point == parsed[6]))
                        if sx == None:
                            counter += 1
                            xx = X(id=counter,
                                   line=parsed[5],
                                   point=parsed[6],
                                   rl=parsed[11],
                                   fr=parsed[12],
                                   tr=parsed[13])
                            session.add(xx)
                            if counter % 100000 == 0:
                                print(counter)
                                session.commit()
                    session.commit()
        except Exception as e:
            print(str(e))
        self.signals.process.emit(counter)
        self.signals.finished.emit(True)


class WorkerSignal(QObject):
    start = pyqtSignal(bool)
    process = pyqtSignal(int)
    process_max = pyqtSignal(int)
    finished = pyqtSignal(bool)
