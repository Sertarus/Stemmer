from PyQt5 import QtCore, QtGui, QtWidgets
import os.path
import re


class StemmerMainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(20, 0, 20, 20)
        self.verticalLayout.setSpacing(10)
        self.LoadEdLabel = QtWidgets.QLabel(self.centralwidget)
        self.verticalLayout.addWidget(self.LoadEdLabel)
        self.LoadEd = QtWidgets.QLineEdit(self.centralwidget)
        self.verticalLayout.addWidget(self.LoadEd)
        self.loadErrorDialog = QtWidgets.QErrorMessage()
        self.DataEdLabel = QtWidgets.QLabel(self.centralwidget)
        self.verticalLayout.addWidget(self.DataEdLabel)
        self.DataEd = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.verticalLayout.addWidget(self.DataEd)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(20, -1, 20, 20)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.SaveEdLabel = QtWidgets.QLabel(self.centralwidget)
        self.verticalLayout_2.addWidget(self.SaveEdLabel)
        self.SaveEd = QtWidgets.QLineEdit(self.centralwidget)
        self.verticalLayout_2.addWidget(self.SaveEd)
        self.ResultEdLabel = QtWidgets.QLabel(self.centralwidget)
        self.verticalLayout_2.addWidget(self.ResultEdLabel)
        self.ResultEd = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.verticalLayout_2.addWidget(self.ResultEd)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menu = QtWidgets.QMenu(self.menubar)
        MainWindow.setMenuBar(self.menubar)
        self.SaveM = QtWidgets.QAction(MainWindow)
        self.SaveM.triggered.connect(self.saveText)
        self.LoadM = QtWidgets.QAction(MainWindow)
        self.LoadM.triggered.connect(self.loadText)
        self.DelM = QtWidgets.QAction(MainWindow)
        self.DelM.triggered.connect(self.removeNonLexicalElements)
        self.SortM = QtWidgets.QAction(MainWindow)
        self.StemM = QtWidgets.QAction(MainWindow)
        self.menuFile.addAction(self.SaveM)
        self.menuFile.addAction(self.LoadM)
        self.menu.addAction(self.DelM)
        self.menu.addAction(self.SortM)
        self.menu.addAction(self.StemM)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Stemmer", "Stemmer"))
        self.LoadEdLabel.setText(_translate("MainWindow", "Путь к загружаемому файлу"))
        self.DataEdLabel.setText(_translate("MainWindow", "Исходные данные"))
        self.SaveEdLabel.setText(_translate("MainWindow", "Путь для записываемого файла"))
        self.ResultEdLabel.setText(_translate("MainWindow", "Результат"))
        self.menuFile.setTitle(_translate("MainWindow", "Файл"))
        self.menu.setTitle(_translate("MainWindow", "Действия"))
        self.SaveM.setText(_translate("MainWindow", "Сохранить"))
        self.LoadM.setText(_translate("MainWindow", "Загрузить"))
        self.DelM.setText(_translate("MainWindow", "Удалить нелексические элеиенты"))
        self.SortM.setText(_translate("MainWindow", "Сортировать"))
        self.StemM.setText(_translate("MainWindow", "Стемминг"))

    def loadText(self):
        if os.path.exists(self.LoadEd.text()):
            fileContent = open(self.LoadEd.text()).read()
            self.DataEd.clear()
            self.DataEd.appendPlainText(fileContent)
        else:
            self.loadErrorDialog.showMessage("Указан некорректный путь к загружаемому файлу.")

    def saveText(self):
        file = open(self.SaveEd.text(), "w")
        file.write(self.ResultEd.toPlainText())
        file.close()

    def removeNonLexicalElements(self):
        text = self.DataEd.toPlainText()
        symbols = ['.', ',', ';', ':', '?', '!', '(', ')', '\"', '\'', '-', '–', '+', '*', '/', '[', ']', '{', '}',
                   '/', '\\', '–', '°', '_' '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        rawWordList = text.split()
        i = 0
        while i != len(rawWordList):
            word = rawWordList[i]
            k = 0
            deletedWord = False
            while k != len(word):
                if word[k] in symbols and (word[k] != '\'' or k == 0 or k == len(word) - 1):
                    if k != 0 and k != len(word) - 1:
                        rawWordList.insert(i + 1, word[k + 1:])
                        word = word[:k]
                        break
                    else:
                        word = word[:k] + word[k+1:]
                        k -= 1
                if word == "":
                    deletedWord = True
                    rawWordList.remove(rawWordList[i])
                    break
                k += 1
            if not deletedWord:
                rawWordList[i] = word
                i += 1
        self.ResultEd.clear()
        for word in rawWordList:
            self.ResultEd.appendPlainText(word)
