import re

from PyQt5 import QtCore, QtWidgets, QtGui
import os.path

from PyQt5.QtWidgets import QInputDialog, QDialog


class StemmerMainWindow(QtWidgets.QWidget):

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
        self.SortM = QtWidgets.QMenu(MainWindow)
        self.SortM1 = QtWidgets.QAction(MainWindow)
        self.SortM1.triggered.connect(self.callSortWords1)
        self.SortM2 = QtWidgets.QAction(MainWindow)
        self.SortM2.triggered.connect(self.callSortWords2)
        self.SortM3 = QtWidgets.QAction(MainWindow)
        self.SortM3.triggered.connect(self.callSortWords3)
        self.SortM4 = QtWidgets.QAction(MainWindow)
        self.SortM4.triggered.connect(self.callSortWords4)
        self.StemM = QtWidgets.QAction(MainWindow)
        self.StemM.triggered.connect(self.makeStemming)
        self.menuFile.addAction(self.SaveM)
        self.menuFile.addAction(self.LoadM)
        self.menu.addAction(self.DelM)
        self.menu.addMenu(self.SortM)
        self.menu.addAction(self.StemM)
        self.SortM.addAction(self.SortM1)
        self.SortM.addAction(self.SortM2)
        self.SortM.addAction(self.SortM3)
        self.SortM.addAction(self.SortM4)
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
        self.SortM.setTitle(_translate("MainWindow", "Сортировать"))
        self.SortM1.setText(_translate("MainWindow", "В прямом порядке, читая слова слева направо"))
        self.SortM2.setText(_translate("MainWindow", "В обратном порядке, читая слова слева направо"))
        self.SortM3.setText(_translate("MainWindow", "В прямом порядке, читая слова справа налево"))
        self.SortM4.setText(_translate("MainWindow", "В обратном порядке, читая слова справа налево"))
        self.StemM.setText(_translate("MainWindow", "Стемминг"))

    def loadText(self):
        if os.path.exists(self.LoadEd.text()):
            fileContent = open(self.LoadEd.text()).read()
            self.DataEd.clear()
            self.DataEd.appendPlainText(fileContent)
        else:
            self.loadErrorDialog.showMessage("Указан некорректный путь к загружаемому файлу.")

    def saveText(self):
        try:
            file = open(self.SaveEd.text(), "w")
            file.write(self.ResultEd.toPlainText())
            file.close()
        except IOError:
            self.loadErrorDialog.showMessage("Указан некорректный путь для сохраняемого файла")

    def removeNonLexicalElements(self):
        text = self.DataEd.toPlainText()
        symbols = ['.', ',', ';', ':', '?', '!', '(', ')', '\"', '\'', '-', '–', '+', '*', '/', '[', ']', '{', '}',
                   '/', '\\', '–', '°', '_', '=', '<', '>', '$', '#', '%', '«', '»']
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
                        word = word[:k] + word[k + 1:]
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

    def sortWords(self, isSortOrderReversed, isReadingOrderReversed):
        data = self.DataEd.toPlainText()
        wordList = data.split("\n")
        sortedList = []
        for word in wordList:
            wordCopy = word.lower()
            if isReadingOrderReversed:
                wordCopy = wordCopy[::-1].lower()
            if not sortedList:
                sortedList.append(word)
            else:
                for i in range(0, len(sortedList)):
                    sortedWordCopy = sortedList[i].lower()
                    if isReadingOrderReversed:
                        sortedWordCopy = sortedWordCopy[::-1]
                    sortedListSize = len(sortedList)
                    for j in range(0, min(len(wordCopy), len(sortedWordCopy))):
                        if wordCopy[j] == sortedWordCopy[j]:
                            if j != min(len(wordCopy), len(sortedWordCopy)) - 1:
                                continue
                            else:
                                if min(len(wordCopy), len(sortedWordCopy)) == len(sortedWordCopy):
                                    if i == len(sortedList) - 1:
                                        sortedList.append(word)
                                        break
                                    else:
                                        break
                                else:
                                    sortedList.insert(i, word)
                                    break

                        else:
                            if wordCopy[j] > sortedWordCopy[j]:
                                if i != len(sortedList) - 1:
                                    break
                                else:
                                    sortedList.append(word)
                                    break
                            else:
                                sortedList.insert(i, word)
                                break
                    if (len(sortedList) != sortedListSize):
                        break
        if isSortOrderReversed:
            sortedList.reverse()
        self.ResultEd.clear()
        for word in sortedList:
            self.ResultEd.appendPlainText(word)

    def callSortWords1(self):
        self.sortWords(False, False)

    def callSortWords2(self):
        self.sortWords(True, False)

    def callSortWords3(self):
        self.sortWords(False, True)

    def callSortWords4(self):
        self.sortWords(True, True)

    def makeStemming(self):
        vowelLetters = ['а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'е']
        consonantLetters = ['б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц',
                            'ч', 'ш', 'щ']
        perfectiveGerund = ["авшись", "явшись", "ившись", "ывшись", "авши", "явши", "ивши", "ывши", "ав",
                            "яв", "ив", "ыв"]
        adjective = ["ими", "ыми", "его", "ого", "ему", "ому", "ее", "ие", "ые", "ое", "ей", "ий", "ый",
                     "ой", "ем", "им", "ым", "ом", "их", "ых", "ую", "юю", "ая", "яя", "ою", "ею"]
        participle = ["аем", "яем", "анн", "янн", "авш", "явш", "ающ", "яющ", "ивш", "ывш", "ующ", "ащ", "ящ"]
        reflexive = ["ся", "сь"]
        verb = ["аете", "яете", "айте", "яйте", "аешь", "яешь", "анно", "янно", "уйте", "ейте", "ала",
                "яла", "ана", "яна", "али", "яли", "аем", "яем", "ало", "яло", "ано", "яно", "ает",
                "яет", "ают", "яют", "аны", "яны", "ать", "ять", "ила", "ыла", "ена", "ите", "или",
                "ыли", "ило", "ыло", "ено", "ует", "уют", "ены", "ить", "ыть", "ишь", "ай", "яй", "ал",
                "ял", "ан", "ян", "ей", "уй", "ил", "ыл", "им", "ым", "ен", "ят", "ит", "ыт", "ую", "ю"]
        noun = ["иями", "ями", "ами", "ией", "иям", "ием", "иях", "ев", "ов", "ие", "ье", "еи", "ии",
                "ей", "ой", "ий", "ям", "ем", "ам", "ом", "ах", "ях", "ию", "ью", "ия", "ья", "а",
                "е", "и", "й", "о", "у", "ы", "ь", "ю", "я"]
        superlative = ["ейше", "ейш"]
        derivational = ["ость", "ост"]
        data = self.DataEd.toPlainText()
        wordList = data.split("\n")
        self.ResultEd.clear()
        for word in wordList:
            wordCopy = word.lower()
            wordCopy.replace('ё', 'е')
            rv = ""
            r1 = ""
            r2 = ""
            isSecondPreviousVowel = False
            isSecondPreviousConsonant = False
            isPreviousVowel = False
            isPreviousConsonant = False
            isCurrentVowel = False
            isCurrentConsonant = False
            for i in range(0, len(wordCopy)):
                isSecondPreviousVowel = isPreviousVowel
                isSecondPreviousConsonant = isPreviousConsonant
                isPreviousVowel = isCurrentVowel
                isPreviousConsonant = isCurrentConsonant
                if wordCopy[i] in vowelLetters:
                    isCurrentVowel = True
                else:
                    isCurrentVowel = False
                if wordCopy[i] in consonantLetters:
                    isCurrentConsonant = True
                else:
                    isCurrentConsonant = False
                if isPreviousVowel and isSecondPreviousConsonant and rv == "":
                    rv = wordCopy[i:]
                if isPreviousConsonant and isSecondPreviousVowel and r1 == "":
                    r1 = wordCopy[i:]
                if r1 != "" and i - (len(word) - len(r1)) >= 2 and isPreviousConsonant and \
                        isSecondPreviousVowel:
                    r2 = wordCopy[i:]
                    break
            rvCopy = rv
            isGoStep2 = False
            deletedEndings = ""
            for ending in perfectiveGerund:
                if wordCopy[len(wordCopy) - len(ending):] == ending:
                    deletedEndings = "-" + ending + deletedEndings
                    wordCopy.replace(ending, "")
                    isGoStep2 = True
                    break
            if not isGoStep2:
                isReflexiveDeleted = False
                for ending in reflexive:
                    if rv[len(rv) - len(ending):] == ending:
                        deletedEndings = "-" + ending + deletedEndings
                        rv = rv.replace(ending, "")
                        isReflexiveDeleted = True
                        break
                for ending in adjective:
                    if rv[len(rv) - len(ending):] == ending:
                        deletedEndings = "-" + ending + deletedEndings
                        rv = rv.replace(ending, "")
                        isGoStep2 = True
                for ending in participle:
                    if rv[len(rv) - len(ending):] == ending:
                        deletedEndings = "-" + ending + deletedEndings
                        rv = rv.replace(ending, "")
                if not isGoStep2:
                    for ending in verb:
                        if rv[len(rv) - len(ending):] == ending:
                            deletedEndings = "-" + ending + deletedEndings
                            rv = rv.replace(ending, "")
                            break
                    if not isReflexiveDeleted:
                        for ending in noun:
                            if rv[len(rv) - len(ending):] == ending:
                                deletedEndings = "-" + ending + deletedEndings
                                rv = rv.replace(ending, "")
                                break
            if len(rv) > 0 and rv[-1] == "и":
                deletedEndings = "-" + "и" + deletedEndings
                rv = rv[:-1]
            for ending in derivational:
                if r2[len(r2) - len(ending):] == ending:
                    deletedEndings = "-" + ending + deletedEndings
                    rv = rv.replace(r2, "")
                    r2 = r2.replace(ending, "")
                    rv += r2
            if (len(rv) > 1 and rv[-2:] == "нн") or (len(rv) > 0 and rv[-1] == "ь"):
                deletedEndings = "-" + rv[-1] + deletedEndings
                rv = rv[:-1]
            for ending in superlative:
                if rv[len(rv) - len(ending):] == ending:
                    deletedEndings = "-" + ending + deletedEndings
                    rv = rv.replace(ending, "")
            if len(rv) > 1 and rv[-2:] == "нн":
                deletedEndings = "н-" + rv[-1] + deletedEndings
            deletedEndingsCopy = deletedEndings.replace("-", "")
            finalWord = re.sub(deletedEndingsCopy + "$", "", wordCopy)
            finalWord += deletedEndings
            finalWord = word[0] + finalWord[1:]
            self.ResultEd.appendPlainText(finalWord)
