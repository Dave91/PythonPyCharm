from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import test


class App(QtWidgets.QMainWindow, test.Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)


def main():
    app = QApplication(sys.argv)
    win = App()
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
