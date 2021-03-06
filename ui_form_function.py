from mainwindowform import Ui_form
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from configure import config
from function import filefunction
from db.dbprocess import PointDbUpdate, XDbUpdate, DbSelectPoint
from db import dbtable
from PyQt5.QtCore import QThreadPool
import logging
from importlib import reload
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_form()
        self.ui.setupUi(self)
        self.threadpool = QThreadPool()

        self.ui.actionDatabase.triggered.connect(self.create_db)
        self.ui.actionQuit.triggered.connect(QtCore.QCoreApplication.instance().quit)
        #
        self.ui.opendb_btn.clicked.connect(self.open_db)
        self.ui.openfile_btn.clicked.connect(self.open_sps)
        #
        self.ui.dbupdate_btn.clicked.connect(self.__update_db)
        self.ui.dataselect_btn.clicked.connect(self.__select_from_db)
        self.ui.quit_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        #
        self.ui.search_btn.clicked.connect(self.__search)
        self.ui.tableclear_btn.clicked.connect(self.clear_tab)

        self.db_file = None
        self.sps_file = None
        self.ui.progressBar.setValue(0)
        self.ui.comboBox.addItems(config.table_dict.keys())

    def create_db(self):
        previous_db_file = self.db_file
        self.db_file = filefunction.file_save(self, previous_db_file, config.db_file_pattern)
        if not self.db_file:
            return

        if not self.db_file.endswith('.sqlite'):
            self.db_file += '.sqlite'

        engine = self.engine_create()
        dbtable.table_create(engine)

    def open_db(self):
        """
            Opens DB file
        """
        try:
            previous_db_file = self.db_file
            self.db_file = filefunction.file_open(self, previous_db_file, config.db_file_pattern)
            self.ui.db_text.setText(self.db_file)
        except Exception as e:
            self.__log(str(e))

    def open_sps(self):
        """
            Opens SPS file
        """
        try:
            previous_sps_file = self.ui.file_text.setText(self.sps_file)
            self.sps_file = filefunction.file_open(self, previous_sps_file, config.r_file_pattern)
            self.ui.file_text.setText(self.sps_file)
            self.__prepare_logging()
            self.to_file = self.sps_file + '.output'
        except Exception as e:
            self.__log(str(e))

    def __update_db(self):
        try:
            engine = self.engine_create()
            dbsession = sessionmaker(bind=engine)
            table = dbtable.choose_table(self.sps_file)
            if table in config.point_table:
                worker = PointDbUpdate(dbsession, self.sps_file)
            else:
                worker = XDbUpdate(dbsession, self.sps_file)
            self.threadpool.start(worker)
            worker.signals.start.connect(self.__process_start)
            worker.signals.process_max.connect(self.__progress_max)
            worker.signals.process.connect(self.__processing)
            worker.signals.finished.connect(self.__processed)
            worker.signals.error.connect(self.__error)
        except Exception as e:
            print('2' + str(e))
            self.__log('update_db :' + str(e))

    def __select_from_db(self):
        try:
            engine = self.engine_create()
            dbsession = sessionmaker(bind=engine)
            worker = DbSelectPoint(dbsession, self.sps_file, self.to_file)
            self.threadpool.start(worker)
            worker.signals.start.connect(self.__process_start)
            worker.signals.process_max.connect(self.__progress_max)
            worker.signals.process.connect(self.__processing)
            worker.signals.finished.connect(self.__processed)
        except Exception as e:
            print(str(e))
            self.__log('select_from_db :' + str(e))

    def __search(self):
        line = float(self.ui.line_text.text())
        point = float(self.ui.point_text.text())
        self.ui.output_text.setText(None)
        try:
            engine = self.engine_create()
            dbsession = sessionmaker(bind=engine)
            _session = dbsession()

            # with _session:
            current_table = self.ui.comboBox.currentText()
            tc = config.table_class[current_table]
            if line > 0 and point > 0:
                data = _session.query(tc).filter(
                    and_(tc.line == line, tc.point == point)).all()
            else:
                data = _session.query(tc).all()
            if len(data) > 0:
                for row in data:
                    self.ui.output_text.append(
                        "%10.1f,%10.1f,%10.1f,%10.1f,%10.1f" % (row.line, row.point, row.x, row.y, row.z))
            else:
                self.ui.output_text.setText('Not exist')
        except Exception as e:
            print(str(e))
            self.__log('update_db :' + str(e))

    def clear_tab(self):
        try:
            self.__btn_enable(False)
            engine = self.engine_create()
            QMessageBox.question(self, 'Question', 'Do you really want to clear database ?',
                                 QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
            if QMessageBox.Yes:
                dbtable.truncate_db(engine)
            self.__btn_enable(True)
        except Exception as e:
            self.__log('clear_tab :' + str(e))

    def __process_start(self, stat: bool):
        self.__btn_enable(stat)
        self.ui.progressBar.setValue(0)

    def __progress_max(self, line_counter):
        self.ui.progressBar.setMaximum(line_counter)
        self.__log('maxline%d' % line_counter)

    def __processing(self, counter):
        self.ui.progressBar.setValue(counter)
        #        self.ui.output_text.append('progress%d' % counter)
        self.__log('progress%d' % counter)

    def __processed(self, stat: bool):
        self.__btn_enable(stat)

    def __error(self, err: str):
        self.__log(err)

    def engine_create(self):
        try:
            engine = create_engine('sqlite:///%s' % self.db_file, connect_args={'check_same_thread': False})
        except Exception as e:
            print(str(e))
        return engine

    def __prepare_logging(self):
        logging.shutdown()
        reload(logging)
        log_filename = self.sps_file + '.log'
        log_format = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
        logging.basicConfig(filename=log_filename, filemode='a', format=log_format, level=logging.NOTSET)
        logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

    def __log(self, msg: str):
        logging.info(msg)

    def __btn_enable(self, stat: bool):
        self.ui.opendb_btn.setEnabled(stat)
        self.ui.openfile_btn.setEnabled(stat)
        self.ui.dbupdate_btn.setEnabled(stat)
        self.ui.dataselect_btn.setEnabled(stat)
        self.ui.quit_btn.setEnabled(stat)
        self.ui.search_btn.setEnabled(stat)
        self.ui.tableclear_btn.setEnabled(stat)
