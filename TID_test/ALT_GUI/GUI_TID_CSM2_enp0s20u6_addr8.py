# pyqt modules
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
# plotting
from pyqtgraph import PlotWidget, plot, mkPen
import pyqtgraph as pg
# miscellaneous modules
import sys
import os
from GUI_PS8_funcs import *
from Ui_MainWindow import *
from ETH_CMD_BASE import *


class MyWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MyWindow, self).__init__(*args, **kwargs)
        self.setObjectName("GUI CSM2 enp0s20u6 ADDR8")
        self.resize(1500, 1000)
        self.initUI()
        return

    # noinspection PyAttributeOutsideInit
    def initUI(self):
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(20, 20, 1450, 950))

        self.tab_func = QtWidgets.QWidget(self)
        self.tabWidget.addTab(self.tab_func, "Functionality GUI")
        self.tab_powersup = QtWidgets.QWidget(self)
        self.tabWidget.addTab(self.tab_powersup, "Power Supply GUI")

        # CSM
        self.tabCSM = QtWidgets.QTabWidget(self.tab_func)
        self.tabCSM.setGeometry(QtCore.QRect(20, 20, 1450, 950))
        #self.CSM_b1 = QtWidgets.QWidget(self)
        #self.tabCSM.addTab(self.CSM_b1, "CSM Board 1")
        #self.eth1 = ETH_control("enp0s20f0u7")
        #self.csm1ui = Ui_MainWindow(self.eth1)
        #self.csm1ui.setupUi(self.CSM_b1, '1, ')

        self.CSM_b2 = QtWidgets.QWidget(self)
        self.tabCSM.addTab(self.CSM_b2, "CSM Board 2")
        self.eth2 = ETH_control("enp0s20f0u6")
        self.csm2ui = Ui_MainWindow(self.eth2)
        self.csm2ui.setupUi(self.CSM_b2, '2, ')

        # Power Supply
        self.tabPS = QtWidgets.QTabWidget(self.tab_powersup)
        self.tabPS.setGeometry(QtCore.QRect(20, 20, 1450, 950))

        self.ps_tab_inst = MyWindowPS()
        self.ps_tab_inst.initUI(self.tabPS, '3, ')

    def normalOutputWritten(self, text):
        if len(text) > 24:
            if text[21:24] == '0, ':
                pass
            #elif text[21:24] == '1, ':
            #    text = text[:21]+text[24:]+'\n'
            #    self.csm1ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
            #    self.csm1ui.textBrowser.insertPlainText(text)
            #    self.logfile = open('lansce_beamrun_CSM1.txt', 'a')
            #    self.logfile.write(text)
            elif text[21:24] == '2, ':
                text = text[:21]+text[24:]+'\n'
                self.csm2ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
                self.csm2ui.textBrowser.insertPlainText(text)
                self.logfile = open('lansce_beamrun_CSM2.txt', 'a')
                self.logfile.write(text)
            elif text[21:24] == '3, ':
                text = text[:21] + text[24:] + '\n'
                self.ps_tab_inst.textBrowser.moveCursor(QtGui.QTextCursor.End)
                self.ps_tab_inst.textBrowser.insertPlainText(text)
                self.logfile = open('lansce_beamrun_PowerSupply.txt', 'a')
                self.logfile.write(text)

class OutLog:
    def __init__(self, edit, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.edit = edit
        self.out = out
        self.color = color

    def write(self, m):
        # if self.color:
        #     tc = self.edit.textColor()
        #     self.edit.setTextColor(self.color)
        # e = datetime.datetime.now()
        # m = "%s %s %s %s:%s:%s>>" %(e.month, e.day, e.year, e.hour, e.minute, e.second) + m
        # m = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ">>" + m
        self.edit.moveCursor(QtGui.QTextCursor.End)
        if m == '\n' :
            self.edit.insertPlainText(m)
        else:
            self.edit.insertPlainText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ">>")
            self.edit.insertPlainText(m)
        # if self.color:
        #     self.edit.setTextColor(tc)
        if self.out:
            self.out.write(m)

    def flush(self):
        pass
#

class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        if text == '\n' :
            text = text
        else:
            text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ">>" + text
        self.textWritten.emit(str(text))

    def flush(self):
        pass

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.stdout = EmittingStream(textWritten=win.normalOutputWritten)
    sys.exit(app.exec_())


window()
