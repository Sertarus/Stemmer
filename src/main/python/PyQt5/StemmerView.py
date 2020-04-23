import sys

from PyQt5.QtWidgets import *

from src.main.python.PyQt5.StemmerMainWindow import StemmerMainWindow


class StemmerView(QMainWindow):

    def __init__(self):
        super(StemmerView, self).__init__()
        self.ui = StemmerMainWindow()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    stemmer = StemmerView()
    stemmer.show()
    sys.exit(app.exec_())