import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
import time
import urllib.request
import lxml
import re
global url,regex
url = ''
regex = ''

class Worker(QThread):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def run(self):
        global url,regex
        if (regex == ''):
            sentence_testing = 'URL = '+url
            self.emit(SIGNAL("ok"),sentence_testing)
            try:
                urltest_request =urllib.request.urlopen(url).read()
                print(urltest_request)
                self.emit(SIGNAL("ok"),'Check URL: OK')
            except:
                self.emit(SIGNAL("ok"),'Check URL: Invalid URL')
        else:
            sentence_testing = 'URL = '+url
            self.emit(SIGNAL("ok"),sentence_testing)
            regex_testing = 'Regular express = '+regex
            self.emit(SIGNAL("ok"),regex_testing)
            urltest_request =urllib.request.urlopen(url).read()
            self.emit(SIGNAL("ok"),'Check URL: OK')
            try:
                decode_html = urltest_request.decode('utf-8')
                self.emit(SIGNAL("ok"),'Check URL: Decoded')
                mo = re.search(regex,decode_html)
                if mo != None:
                    check_result = 'Version Found : %s'% mo.group(1)
                    self.emit(SIGNAL("ok"),check_result)
                else:
                    self.emit(SIGNAL("ok"),'Search result : Fail')
            except:
                self.emit(SIGNAL("ok"),'Check URL: Decode Fail\n')

        self.emit(SIGNAL("ok"),'Waiting......\n')


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setWindowTitle('--Url testing--')
        self.resize(799, 669)
        self.text = QtGui.QTextBrowser()
        self.text.setGeometry(QtCore.QRect(20, 10, 761, 401))
        self.urledit = QtGui.QLineEdit('Input your URL')
        self.urledit.setGeometry(QtCore.QRect(140, 430, 641, 31))
        self.regexedit = QtGui.QLineEdit('Input your regex')
        self.regexedit.setGeometry(QtCore.QRect(140, 480, 641, 31))
        self.run = QtGui.QPushButton('Run')
        self.run.setGeometry(QtCore.QRect(260, 530, 241, 81))
        self.label = QtGui.QLabel('Input URL:')
        self.label.setGeometry(QtCore.QRect(40, 430, 81, 31))
        self.label_2 = QtGui.QLabel('Input Regex')
        self.label_2.setGeometry(QtCore.QRect(20, 480, 101, 31))

        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.urledit)
        layout.addWidget(self.regexedit)
        #layout.addWidget(self.label)
        #layout.addWidget(self.label_2)
        layout.addWidget(self.run)
        self.setLayout(layout)

        self.work = Worker()
        # SIGNAL&SLOT
        self.run.clicked.connect(self.start)
        self.connect(self.work, SIGNAL("ok"),self.updateUI)
    def start(self):
        global url,regex
        url = self.urledit.text()
        regex = self.regexedit.text()
        self.work.start()
        #self.run.setEnabled(False)
    def updateUI(self,status):
        self.text.append('[STATUS]:%s'%(status))

app = QApplication(sys.argv)
QQ = MainWindow()
QQ.show()
app.exec_()