from PyQt5.QtWidgets import QApplication
from ui_form_function import MainWindow


def main():
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
