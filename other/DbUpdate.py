import os
import time
from PyQt5.QtWidgets import QDialog, QFileDialog
from UIDbUpdateForm import Ui_DbUpdateForm
import dbupdate
import check


class DbUpdate(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_DbUpdateForm()
        self.ui.setupUi(self)

        self.ui.btnOpenDb.clicked.connect(self.clicked_btn_open_db)
        self.ui.btnOpenSPS.clicked.connect(self.clicked_btn_open_sps)
        self.ui.btnProcess.clicked.connect(self.clicked_btn_process)
        self.ui.btnRemoveSPS.clicked.connect(self.clicked_btn_remove_sps)
        self.ui.comboFileType.addItem('SPS 2.1')
        self.ui.lblStatus.setText('')

        self.db_file = None

    def clicked_btn_open_db(self):
        """
            Opens DB file
        """
        self.db_file, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "SQLite (*.sqlite );;All files (*.*)",
            # options=QFileDialog.DontUseNativeDialog
        )

        if not self.db_file:
            return

        self.ui.listDb.clear()
        self.ui.listDb.addItem(self.db_file)

    def clicked_btn_open_sps(self):
        """
            Opens SPS file
        """
        sps_file, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "SPS Source (*.S *.SPS *.s *.sps);;SPS Receiver (*.R *.RPS *.r *.rps);;All files (*.*)",
            # options=QFileDialog.DontUseNativeDialog
        )

        if not sps_file:
            return

        self.ui.listSPS.addItem(sps_file)

    def clicked_btn_remove_sps(self):
        for i in self.ui.listSPS.selectedItems():
            self.ui.listSPS.takeItem(self.ui.listSPS.row(i))

    def clicked_btn_process(self):
        """
            Process
        """
        self.ui.lblStatus.setText('')
        self.ui.btnProcess.setDisabled(True)
        self.ui.btnDone.setDisabled(True)
        start_time = time.time()
        sps_files = [str(self.ui.listSPS.item(i).text()) for i in range(self.ui.listSPS.count())]

        if self.db_file and len(sps_files) > 0:

            for sps_file in sps_files:
                line_numbers = check.count_file_line_number(sps_file)
                self.ui.progressBar.setMaximum(line_numbers)
                result = dbupdate.process(self.ui.progressBar, self.db_file, sps_file)
                msg = "%s, %d, %.2fs" \
                      % (os.path.basename(sps_file), result, time.time() - start_time)
                self.ui.lblStatus.setText(msg)

        self.ui.btnProcess.setEnabled(True)
        self.ui.btnDone.setEnabled(True)
