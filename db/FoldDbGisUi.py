import csv
from sqlalchemy.orm import sessionmaker
from PyQt5.QtWidgets import QTextBrowser, QProgressBar

from SeismicFoldDbGisUi.entity.Bin import Bin


class FoldDbGisUi:

    def __init__(self, db_engine, commit_every=10000):
        self.__db_engine = db_engine
        self._commit_every = commit_every

    def create_table(self):
        Bin.__table__.create(self.__db_engine)

    def delete_table(self):
        # Bin.__table__.drop(self.__db_engine)
        Bin.__table__.drop(self.__db_engine)

    @staticmethod
    def _create_bin_from_csv_record(record: list):
        b = Bin(
            binn=int(record[3]),
            fold=int(record[2]),
            geom="POINT (%.1f %.1f)" % (float(record[0]), float(record[1]))
        )

        return b

    def _create_session(self):
        sess_mkr = sessionmaker()
        sess_mkr.configure(bind=self.__db_engine)
        return sess_mkr()

    @staticmethod
    def _count_file_line_number(filename: str):
        return sum(1 for line in open(filename))

    @staticmethod
    def timer(start, end):
        """ timer """
        hours, rem = divmod(end - start, 3600)
        minutes, seconds = divmod(rem, 60)
        return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)
