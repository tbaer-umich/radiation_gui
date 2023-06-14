#GUI pyqt5 module
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5 import QtWidgets, QtCore 
from PyQt5.QtWidgets import QApplication, QMainWindow
#plotting
from pyqtgraph import PlotWidget, plot, mkPen
import pyqtgraph as pg

import sys
import os

#from ps_funcs import comm, PS_on, PS_off, IV_meas
from ps_funcs_ps5 import comm5, PS_on5, PS_off5, IV_meas5
#from ps_funcs_ps8 import comm8, PS_on8, PS_off8, IV_meas8
import datetime 
import time 
#from matplotlib.backends.qt_compat import QtCore, QtWidgets 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from  matplotlib.figure import Figure 
from  matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
import matplotlib.pyplot as plt 
import numpy as np
import threading 
import traceback
import csv
'''
date = '0805'
condition = 'beam_run'
PS5_CSM1_csvname = 'CSM1_'+date+'_'+condition+'.csv'
PS8_CSM2_csvname = 'CSM2_'+date+'_'+condition+'.csv'
PS5_CSM1_txtname = 'CSM1_'+date+'_'+condition+'.txt'
PS8_CSM2_txtname = 'CSM2_'+date+'_'+condition+'.txt'
'''


class PSWorker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    #all_data = pyqtSignal(float, float, float, float, int, object)
    all_data_5 = pyqtSignal(float, float, float, float, int, object)
    #GUI_PS8 = pyqtSignal(float, float, float, float)
    GUI_PS5 = pyqtSignal(float, float, float, float) 

    def __init__(self, MyWindow, identifier):
        super(PSWorker, self).__init__()
        self.MyWindow = MyWindow 
        self.MyWindow.processing = True
        self.identifier = identifier

    def run(self):
        self.MyWindow.time_last = 0
        time_accu = self.MyWindow.time_total 
        print(self.identifier+"Start Monitoring")
        start = time.time()
        self.target_time = datetime.datetime.now()
        while self.MyWindow.processing: 
            self.target_time = self.target_time + datetime.timedelta(seconds=60)
            while self.MyWindow.device_release==0:
                pass
            self.MyWindow.device_release=0
            #self.data = IV_meas8()
            self.data_ps5 = IV_meas5()
            self.MyWindow.device_release = 1
            time.sleep(2)
            end = time.time()
            self.MyWindow.time_last = end - start 
            #print(type(self.MyWindow.time_last))
            #self.GUI_PS8.emit(self.data[0][0], self.data[1][0], self.data[2][0], self.data[3][0])
            self.GUI_PS5.emit(self.data_ps5[0][0], self.data_ps5[1][0], self.data_ps5[2][0], self.data_ps5[3][0])
            #self.all_data.emit(self.data[0][0], self.data[1][0], self.data[2][0], self.data[3][0], int(self.MyWindow.time_last), self.target_time)
            self.all_data_5.emit(self.data_ps5[0][0], self.data_ps5[1][0], self.data_ps5[2][0], self.data_ps5[3][0], int(self.MyWindow.time_last), self.target_time)
            self.MyWindow.time_total = time_accu + self.MyWindow.time_last 

        print(self.identifier+"End Monitoring")
        print(self.identifier+"Monitoring Time: " + str(end-start))
        self.finished.emit()
        return 

    def stop(self):
        self.MyWindow.processing = False


class MyWindowPS(object):
    def __init__(self):
        self.time_total = 0
        self.processing = False
        self.device_release = 1
        self.date_txt = 'BNL'
        self.condition_txt = 'beam_run'
        self.PS5_CSM1_csvname = 'CSM1_' + self.date_txt + '_' + self.condition_txt + '.csv'
        #self.PS8_CSM2_csvname = 'CSM2_' + self.date_txt + '_' + self.condition_txt + '.csv'
        self.PS5_CSM1_txtname = 'CSM1_' + self.date_txt + '_' + self.condition_txt + '.txt'
        #self.PS8_CSM2_txtname = 'CSM2_' + self.date_txt + '_' + self.condition_txt + '.txt'
        return 

    def initUI(self, MainWindow, identifier):
        #self.volt1 = []
        #self.volt2 = []
        #self.curr1 = []
        #self.curr2 = []
        #self.time = []
        #self.date = []
        self.volt1_5 = []
        self.volt2_5 = []
        self.curr1_5 = []
        self.curr2_5 = []
        self.time_5 = []
        self.date_5 = []
        self.identifier = identifier

        #tabs 
        self.tabWidget = QtWidgets.QTabWidget(MainWindow)
        self.tabWidget.setGeometry(QtCore.QRect(100, 30, 300,300))

        #self.tab_PS_1_addr8 = QtWidgets.QWidget(MainWindow)
        #self.tabWidget.addTab(self.tab_PS_1_addr8, "PS1:Addr8")
        self.tab_PS_2_addr5 = QtWidgets.QWidget(MainWindow)
        self.tabWidget.addTab(self.tab_PS_2_addr5, "PS2:Addr5")

        # general printout layout
        self.logLayoutWdiget = QtWidgets.QWidget(MainWindow)
        self.logLayoutWdiget.setGeometry(QtCore.QRect(20, 450, 500, 400))  # (left, top, width, height)
        self.logLayout = QtWidgets.QVBoxLayout(self.logLayoutWdiget)
        self.logLayout.setContentsMargins(0, 0, 0, 0)

        self.label = QtWidgets.QLabel("Run Info", self.logLayoutWdiget)
        self.logLayout.addWidget(self.label)
        self.textBrowser = QtWidgets.QTextBrowser(self.logLayoutWdiget)
        self.logLayout.addWidget(self.textBrowser)

        #PS1:ADDR8 
        #self.layoutWidget = QtWidgets.QWidget(self.tab_PS_1_addr8)
        #self.layoutWidget.setGeometry(QtCore.QRect(30,70,200,150))
        #self.layout = QtWidgets.QVBoxLayout(self.layoutWidget)

        #self.layoutWidget2 = QtWidgets.QWidget(self.tab_PS_1_addr8)
        #self.layoutWidget2.setGeometry(QtCore.QRect(150,70,200,150))
        #self.layout2 = QtWidgets.QVBoxLayout(self.layoutWidget2)

        #self.layoutWidget3 = QtWidgets.QWidget(self.tab_PS_1_addr8)
        #self.layoutWidget3.setGeometry(QtCore.QRect(50,-20,200,150))
        #self.layout3 = QtWidgets.QVBoxLayout(self.layoutWidget3)

        #self.layoutWidget4 = QtWidgets.QWidget(self.tab_PS_1_addr8)
        #self.layoutWidget4.setGeometry(QtCore.QRect(25,170,130,150))
        #self.layout4 = QtWidgets.QVBoxLayout(self.layoutWidget4)

        #self.layoutWidget5 = QtWidgets.QWidget(self.tab_PS_1_addr8)
        #self.layoutWidget5.setGeometry(QtCore.QRect(150,170,130,150))
        #self.layout5 = QtWidgets.QVBoxLayout(self.layoutWidget5)

        #PS2:ADDR5 
        self.layoutWidget12 = QtWidgets.QWidget(self.tab_PS_2_addr5)
        self.layoutWidget12.setGeometry(QtCore.QRect(30,70,200,150))
        self.layout12 = QtWidgets.QVBoxLayout(self.layoutWidget12)

        self.layoutWidget13 = QtWidgets.QWidget(self.tab_PS_2_addr5)
        self.layoutWidget13.setGeometry(QtCore.QRect(150,70,200,150))
        self.layout13 = QtWidgets.QVBoxLayout(self.layoutWidget13)

        self.layoutWidget14 = QtWidgets.QWidget(self.tab_PS_2_addr5)
        self.layoutWidget14.setGeometry(QtCore.QRect(50,-20,200,150))
        self.layout14 = QtWidgets.QVBoxLayout(self.layoutWidget14)
    
        self.layoutWidget15 = QtWidgets.QWidget(self.tab_PS_2_addr5)
        self.layoutWidget15.setGeometry(QtCore.QRect(25,170,130,150))
        self.layout15 = QtWidgets.QVBoxLayout(self.layoutWidget15)

        self.layoutWidget16 = QtWidgets.QWidget(self.tab_PS_2_addr5)
        self.layoutWidget16.setGeometry(QtCore.QRect(150,170,130,150))
        self.layout16 = QtWidgets.QVBoxLayout(self.layoutWidget16)

        #MONITOR ON/OFF
        self.layoutWidget10 = QtWidgets.QWidget(MainWindow)
        self.layoutWidget10.setGeometry(QtCore.QRect(100,310,150,150))
        self.layout10 = QtWidgets.QVBoxLayout(self.layoutWidget10)

        self.layoutWidget11 = QtWidgets.QWidget(MainWindow)
        self.layoutWidget11.setGeometry(QtCore.QRect(250,310,150,150))
        self.layout11 = QtWidgets.QVBoxLayout(self.layoutWidget11)
        
        #plot layout PS8
        #self.layoutWidget6 = QtWidgets.QWidget(MainWindow)
        #self.layoutWidget6.setGeometry(QtCore.QRect(350, 20, 400, 250))
        #self.layout6 = QtWidgets.QHBoxLayout(self.layoutWidget6)

        ##self.layoutWidget7 = QtWidgets.QWidget(self)
        ##self.layoutWidget7.setGeometry(QtCore.QRect(690, 20, 370, 250))
        ##self.layout7 = QtWidgets.QHBoxLayout(self.layoutWidget7)

        #self.layoutWidget8 = QtWidgets.QWidget(MainWindow)
        #self.layoutWidget8.setGeometry(QtCore.QRect(750, 20, 400, 250)) #1050, 20, 370, 250
        #self.layout8 = QtWidgets.QHBoxLayout(self.layoutWidget8)

        ##self.layoutWidget9 = QtWidgets.QWidget(self)
        ##self.layoutWidget9.setGeometry(QtCore.QRect(330, 280, 370, 250))
        ##self.layout9 = QtWidgets.QHBoxLayout(self.layoutWidget9)
        
        #plot layout PS5
        self.layoutWidget17 = QtWidgets.QWidget(MainWindow)
        self.layoutWidget17.setGeometry(QtCore.QRect(550, 10, 800, 450)) #690, 280, 370, 250
        self.layout17 = QtWidgets.QHBoxLayout(self.layoutWidget17)

        #self.layoutWidget18 = QtWidgets.QWidget(self)
        #self.layoutWidget18.setGeometry(QtCore.QRect(1050, 280, 370, 250))
        #self.layout18 = QtWidgets.QHBoxLayout(self.layoutWidget18)

        self.layoutWidget19 = QtWidgets.QWidget(MainWindow)
        self.layoutWidget19.setGeometry(QtCore.QRect(550, 450, 800, 450)) #350, 540, 370, 250
        self.layout19 = QtWidgets.QHBoxLayout(self.layoutWidget19)

        #self.layoutWidget20 = QtWidgets.QWidget(self)
        #self.layoutWidget20.setGeometry(QtCore.QRect(710, 540, 370, 250))
        #self.layout20 = QtWidgets.QHBoxLayout(self.layoutWidget20)

        #IV labels PS1:ADDR8
        #self.label = QtWidgets.QLabel(self.layoutWidget)
        #self.label.setText("Voltage1 (V):")
        #self.layout.addWidget(self.label)

        #self.label1 = QtWidgets.QLabel(self.layoutWidget)
        #self.label1.setText("Voltage2 (V):")
        #self.layout.addWidget(self.label1)

        #self.label2 = QtWidgets.QLabel(self.layoutWidget)
        #self.label2.setText("Current1 (A):")
        #self.layout.addWidget(self.label2)

        #self.label3 = QtWidgets.QLabel(self.layoutWidget)
        #self.label3.setText("Current2 (A):")
        #self.layout.addWidget(self.label3)
        

        #IV labels PS2:ADDR5
        self.label8 = QtWidgets.QLabel(self.layoutWidget12)
        self.label8.setText("Voltage1 (V):")
        self.layout12.addWidget(self.label8)

        self.label9 = QtWidgets.QLabel(self.layoutWidget12)
        self.label9.setText("Voltage2 (V):")
        self.layout12.addWidget(self.label9)

        self.label10 = QtWidgets.QLabel(self.layoutWidget12)
        self.label10.setText("Current1 (A):")
        self.layout12.addWidget(self.label10)

        self.label11 = QtWidgets.QLabel(self.layoutWidget12)
        self.label11.setText("Current2 (A):")
        self.layout12.addWidget(self.label11)

        #Read IV labels PS1:ADDR8
        #self.label4 = QtWidgets.QLabel(self.layoutWidget2)
        #self.label4.setText("-")
        #self.layout2.addWidget(self.label4)

        #self.label5 = QtWidgets.QLabel(self.layoutWidget2)
        #self.label5.setText("-")
        #self.layout2.addWidget(self.label5)

        #self.label6 = QtWidgets.QLabel(self.layoutWidget2)
        #self.label6.setText("-")
        #self.layout2.addWidget(self.label6)

        #self.label7 = QtWidgets.QLabel(self.layoutWidget2)
        #self.label7.setText("-")
        #self.layout2.addWidget(self.label7)
        
        #Read IV labels PS2:ADDR5
        self.label12 = QtWidgets.QLabel(self.layoutWidget13)
        self.label12.setText("-")
        self.layout13.addWidget(self.label12)

        self.label13 = QtWidgets.QLabel(self.layoutWidget13)
        self.label13.setText("-")
        self.layout13.addWidget(self.label13)

        self.label14 = QtWidgets.QLabel(self.layoutWidget13)
        self.label14.setText("-")
        self.layout13.addWidget(self.label14)

        self.label15 = QtWidgets.QLabel(self.layoutWidget13)
        self.label15.setText("-")
        self.layout13.addWidget(self.label15)

        #pushbutton ps
        #self.b1 = QtWidgets.QPushButton(self.layoutWidget3)
        #self.b1.setText("Init Power Supply")
        #self.layout3.addWidget(self.b1)
        #self.b1.clicked.connect(self.gpib)
       
        self.b6 = QtWidgets.QPushButton(self.layoutWidget14)
        self.b6.setText("Init Power Supply")
        self.layout14.addWidget(self.b6)
        self.b6.clicked.connect(self.gpib_5)

        #self.b2 = QtWidgets.QPushButton(self.layoutWidget4)
        #self.b2.setText("PS ON")
        #self.layout4.addWidget(self.b2)
        #self.b2.clicked.connect(self.pwr_on)

        self.b7 = QtWidgets.QPushButton(self.layoutWidget15)
        self.b7.setText("PS ON")
        self.layout15.addWidget(self.b7)
        self.b7.clicked.connect(self.pwr_on_5)

        #self.b3 = QtWidgets.QPushButton(self.layoutWidget5)
        #self.b3.setText("PS OFF")
        #self.layout5.addWidget(self.b3)
        #self.b3.clicked.connect(self.pwr_off)
        #self.b3.setEnabled(False)

        self.b8 = QtWidgets.QPushButton(self.layoutWidget16)
        self.b8.setText("PS OFF")
        self.layout16.addWidget(self.b8)
        self.b8.clicked.connect(self.pwr_off_5)
        self.b8.setEnabled(False)

        self.b4 = QtWidgets.QPushButton(self.layoutWidget10)
        self.b4.setText("MONITOR ON")
        self.layout10.addWidget(self.b4)
        self.b4.clicked.connect(self.monitor_on)
        
        self.b5 = QtWidgets.QPushButton(self.layoutWidget11)
        self.b5.setText("MONITOR OFF")
        self.layout11.addWidget(self.b5)
        self.b5.clicked.connect(self.monitor_off)
        self.b5.setEnabled(False)

        #pyqtgraph
        #self.graphWidget = pg.PlotWidget()
        self.pen = pg.mkPen(color="k", width=2)
        #self.layout6.addWidget(self.graphWidget)
        #self.graphWidget.setBackground('w')
        #self.graphWidget.setTitle("PS1:ADDR8_CSM2 Volt1 vs Time (sec)", color="b", size="10pt")
        #self.graphWidget.setLabel('left', 'Volt1 (V)', color="r", size="5pt")
        #self.graphWidget.setLabel('bottom', 'Time (S)', color="r", size="5pt")
        #self.graphWidget.showGrid(x=True, y=True)

        #self.data_line =  self.graphWidget.plot(self.time, self.volt1, pen = self.pen)

        ##self.graphWidget1 = pg.PlotWidget()
        ##self.layout7.addWidget(self.graphWidget1)
        ##self.graphWidget1.setBackground('w')
        ##self.graphWidget1.setTitle("PS1:ADDR8 Volt2 vs Time (sec)", color="b", size="10pt")
        ##self.graphWidget1.setLabel('left', 'Volt2 (V)', color="r", size="5pt")
        ##self.graphWidget1.setLabel('bottom', 'Time (S)', color="r", size="5pt")
        ##self.graphWidget1.showGrid(x=True, y=True)
        
        #self.graphWidget2 = pg.PlotWidget()
        #self.layout8.addWidget(self.graphWidget2)
        #self.graphWidget2.setBackground('w')
        #self.graphWidget2.setTitle("PS1:ADDR8_CSM2 Curr1 vs Time (sec)", color="b", size="10pt")
        #self.graphWidget2.setLabel('left', 'Curr1 (A)', color="r", size="5pt")
        #self.graphWidget2.setLabel('bottom', 'Time (S)', color="r", size="5pt")
        #self.graphWidget2.showGrid(x=True, y=True)

        #self.data_line2 = self.graphWidget2.plot(self.time, self.curr1, pen = self.pen)

        ##self.graphWidget3 = pg.PlotWidget()
        ##self.layout9.addWidget(self.graphWidget3)
        ##self.graphWidget3.setBackground('w')
        ##self.graphWidget3.setTitle("PS1:ADDR8 Curr2 vs Time (sec)", color="b", size="10pt")
        ##self.graphWidget3.setLabel('left', 'Curr2 (A)', color="r", size="5pt")
        ##self.graphWidget3.setLabel('bottom', 'Time (S)', color="r", size="5pt")
        ##self.graphWidget3.showGrid(x=True, y=True)
       
        #plot PS5
        self.graphWidget4 = pg.PlotWidget()
        self.layout17.addWidget(self.graphWidget4)
        self.graphWidget4.setBackground('w')
        self.graphWidget4.setTitle("PS2:ADDR5_CSM1 Volt1 vs Time (sec)", color="b", size="10pt")
        self.graphWidget4.setLabel('left', 'Volt1 (V)', color="r", size="5pt")
        self.graphWidget4.setLabel('bottom', 'Time (S)', color="r", size="5pt")
        self.graphWidget4.showGrid(x=True, y=True)

        self.data_line4 = self.graphWidget4.plot(self.time_5, self.volt1_5, pen = self.pen)

        #self.graphWidget5 = pg.PlotWidget()
        #self.layout18.addWidget(self.graphWidget5)
        #self.graphWidget5.setBackground('w')
        #self.graphWidget5.setTitle("PS2:ADDR5 Volt2 vs Time (sec)", color="b", size="10pt")
        #self.graphWidget5.setLabel('left', 'Volt2 (V)', color="r", size="5pt")
        #self.graphWidget5.setLabel('bottom', 'Time (S)', color="r", size="5pt")
        #self.graphWidget5.showGrid(x=True, y=True)

        self.graphWidget6 = pg.PlotWidget()
        self.layout19.addWidget(self.graphWidget6)
        self.graphWidget6.setBackground('w')
        self.graphWidget6.setTitle("PS2:ADDR5_CSM1 Curr1 vs Time (sec)", color="b", size="10pt")
        self.graphWidget6.setLabel('left', 'Curr1 (A)', color="r", size="5pt")
        self.graphWidget6.setLabel('bottom', 'Time (S)', color="r", size="5pt")
        self.graphWidget6.showGrid(x=True, y=True)

        self.data_line6 = self.graphWidget6.plot(self.time_5, self.curr1_5, pen = self.pen)

        #self.graphWidget7 = pg.PlotWidget()
        #self.layout20.addWidget(self.graphWidget7)
        #self.graphWidget7.setBackground('w')
        #self.graphWidget7.setTitle("PS2:ADDR5 Curr2 vs Time (sec)", color="b", size="10pt")
        #self.graphWidget7.setLabel('left', 'Curr2 (A)', color="r", size="5pt")
        #self.graphWidget7.setLabel('bottom', 'Time (S)', color="r", size="5pt")
        #self.graphWidget7.showGrid(x=True, y=True)


        #self.timer = QtCore.QTimer()
        #self.timer.setInterval(50)
        #self.timer.timeout.connect(self.update_plot_data)
        #self.timer.start()

    def gpib_5(self, addr):
        self.gpib_inst5 = comm5('5')
        print(self.identifier+"Power supply 5 connected to GPIB")
        with open(self.PS5_CSM1_txtname, "a") as f:
            dgpib5 = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
            f.write("%s %s" % (dgpib5, "Power Supply Connected to GPIB") + '\n')
            f.close()
        self.b6.setEnabled(False)

    def pwr_on_5(self):
        while self.device_release == 0:
            pass
        self.device_release = 0
        self.ON5 = PS_on5()
        self.device_release = 1
        print(self.identifier+'OUTP ON PS5')
        time.sleep(3)
        with open(self.PS5_CSM1_txtname, "a") as f:
            dop = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
            f.write("%s %s" % (dop, "OUTP ON") + '\n')
            f.close()
        self.b7.setEnabled(False)
        self.b8.setEnabled(True)

    def pwr_off_5(self):
        while self.device_release == 0:
            pass
        self.device_release = 0
        self.OFF5 = PS_off5()
        self.device_release = 1
        print(self.identifier+'OUTP OFF PS5')
        time.sleep(3)
        with open(self.PS5_CSM1_txtname, "a") as f:
            doff = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
            f.write("%s %s" % (doff, "OUTP OFF") + '\n')
            f.close()
        self.b8.setEnabled(False)
        self.b7.setEnabled(True)

    #def gpib(self, addr): # dont know if it works yet
    #    self.gpib_inst = comm8('8')
    #    print(self.identifier+"Power supply 8 connected to GPIB")
    #    with open(self.PS8_CSM2_txtname, "a") as f:
    #        d = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    #        f.write("%s %s" % (d, "Power Supply Connected to GPIB") + '\n')
    #        f.close()
    #    self.b1.setEnabled(False)
    
    #def pwr_on(self):
    #    while self.device_release == 0:
    #        pass
    #    self.device_release = 0
    #    self.ON = PS_on8()
    #    self.device_release = 1
    #    print(self.identifier+'OUTP ON PS8')
    #    time.sleep(3)
    #    with open(self.PS8_CSM2_txtname, "a") as f:
    #        dop = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    #        f.write("%s %s" % (dop, "OUTP ON") + '\n')
    #        f.close()
    #    self.b2.setEnabled(False)
    #    self.b3.setEnabled(True)
    
    #def pwr_off(self):
    #    while self.device_release == 0:
    #        pass
    #    self.device_release = 0
    #    self.OFF = PS_off8()
    #    self.device_release = 1
    #    print(self.identifier+'OUTP OFF PS8')
    #    time.sleep(3)
    #    with open(self.PS8_CSM2_txtname, "a") as f:
    #        doff = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    #        f.write("%s %s" % (doff, "OUTP OFF") + '\n')
    #        f.close()
    #    self.b3.setEnabled(False)
    #    self.b2.setEnabled(True)
        
    def monitor_on(self):
        #self.volt1 = []
        #self.volt2 = []
        #self.curr1 = []
        #self.curr2 = []
        #self.time = []
        #self.date = []

        self.volt1_5 = []
        self.volt2_5 = []
        self.curr1_5 = []
        self.curr2_5 = []
        self.time_5 = []
        self.date_5 = []

        self.thread = QThread()
        self.worker = PSWorker(self, self.identifier)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        #self.worker.all_data.connect(self.graph)
        self.worker.all_data_5.connect(self.graph_5)
        #self.worker.GUI_PS8.connect(self.label_func)
        self.worker.GUI_PS5.connect(self.label5_func) 
        self.thread.start()
        self.b4.setEnabled(False)
        self.b5.setEnabled(True)
        self.thread.finished.connect(lambda: self.b4.setEnabled(True))
        self.thread.finished.connect(lambda: self.b5.setEnabled(False))
        self.thread.finished.connect(self.monitor_off)
        with open(self.PS5_CSM1_txtname, "a") as f:
            d1 = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
            f.write("%s %s" %(d1, "Power Supply  ON") + '\n')
            f.close()
        return

    #def label_func(self, par1, par2, par3, par4):
    #    print("Label GUI PS8")
    #    self.label4.setText("%.5f"%(par1))
    #    self.label5.setText("%.5f"%(par2))
    #    self.label6.setText("%.5f"%(par3))
    #    self.label7.setText("%.5f"%(par4))
    #    print(self.identifier+"PS 8 Volt1: "+"%.5f"%(par1))
    #    print(self.identifier+"PS 8 Volt2: "+"%.5f"%(par2))
    #    print(self.identifier+"PS 8 Curr1: "+"%.5f"%(par3))
    #    print(self.identifier+"PS 8 Curr2: "+"%.5f"%(par4))
    #    return par1, par2, par3, par4

    def label5_func(self, val1, val2, val3, val4):
        print("Label GUI PS5")
        self.label12.setText("%.5f"%(val1))
        self.label13.setText("%.5f"%(val2))
        self.label14.setText("%.5f"%(val3))
        self.label15.setText("%.5f"%(val4))
        print(self.identifier + "PS 5 Volt1: " + "%.5f" % (val1))
        print(self.identifier + "PS 5 Volt2: " + "%.5f" % (val2))
        print(self.identifier + "PS 5 Curr1: " + "%.5f" % (val3))
        print(self.identifier + "PS 5 Curr2: " + "%.5f" % (val4))
        return val1, val2, val3, val4

    #def graph(self, f1, f2, f3, f4, i1, obj1):
    #    print("Get Data PS8")
    #    self.volt1.append(f1)
    #    self.volt2.append(f2)
    #    self.curr1.append(f3)
    #    self.curr2.append(f4)
    #    self.time.append(i1)
    #    self.date.append(obj1)

    #    if len(self.time) > 30:
    #        self.volt1 = self.volt1[1:]
    #        self.volt2 = self.volt2[1:]
    #        self.curr1 = self.curr1[1:]
    #        self.curr2 = self.curr2[1:]
    #        self.time = self.time[1:]
    #        self.date = self.date[1:]
        '''
        self.data_line =  self.graphWidget.plot(self.time, self.volt1, pen = self.pen)
        #self.data_line1 = self.graphWidget1.plot(self.time, self.volt2, pen = self.pen)
        self.data_line2 = self.graphWidget2.plot(self.time, self.curr1, pen = self.pen)
        #self.data_line3 = self.graphWidget3.plot(self.time, self.curr2, pen = self.pen)
        '''

    #    self.data_line.setData(self.time,self.volt1)
    #    self.data_line2.setData(self.time,self.curr1)

    #    d2 = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    #    with open(self.PS8_CSM2_csvname, 'a') as csv_file:
    #        fieldnames = ['DateTime','Time_S', 'Volt1_V', 'Volt2_V', 'Curr1_A', 'Curr2_A']
    #        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    #        writer.writeheader()
    #        writer.writerow({'DateTime': d2, 'Time_S': str(i1), 'Volt1_V': str(f1), 'Volt2_V': str(f2), 'Curr1_A': str(f3), 'Curr2_A': str(f4)})

    #    with open(self.PS8_CSM2_txtname, "a") as f:
            ##d2 = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    #        f.write("%s %s" %(d2, "Get IV Data") + '\n')
    #        f.write("%s %s %s" % (d2, "Volt1 (V): ", str(f1) +  '\n'))
    #        f.write("%s %s %s" % (d2, "Volt2 (V): ", str(f2) + '\n'))
    #        f.write("%s %s %s" % (d2, "Curr1 (A): ", str(f3) + '\n'))
    #        f.write("%s %s %s" % (d2, "Curr2 (A): ", str(f4) + '\n'))
    #        f.write("%s %s %s" % (d2, "Time (Sec): ", str(i1) + '\n'))
            ##f.write("%s %s %s" % (d2, "Date: ", str(obj1) + '\n' ))
    #        f.close()

    #    return
        #return self.data_line, self.data_line1, self.data_line2, self.data_line3 

    def graph_5(self, f1_5, f2_5, f3_5, f4_5, i1_5, obj1_5):
        print("Get Data PS5")
        self.volt1_5.append(f1_5)
        self.volt2_5.append(f2_5)
        self.curr1_5.append(f3_5)
        self.curr2_5.append(f4_5)
        self.time_5.append(i1_5)
        self.date_5.append(obj1_5)

        if len(self.time_5) > 30:
            self.volt1_5 = self.volt1_5[1:]
            self.volt2_5 = self.volt2_5[1:]
            self.curr1_5 = self.curr1_5[1:] 
            self.curr2_5 = self.curr2_5[1:]
            self.time_5 = self.time_5[1:] 
            self.date_5 = self.date_5[1:] 
        
        '''
        self.data_line4 = self.graphWidget4.plot(self.time_5, self.volt1_5, pen = self.pen)
        #self.data_line5 = self.graphWidget5.plot(self.time_5, self.volt2_5, pen = self.pen)
        self.data_line6 = self.graphWidget6.plot(self.time_5, self.curr1_5, pen = self.pen)
        #self.data_line7 = self.graphWidget7.plot(self.time_5, self.curr2_5, pen = self.pen)
        '''

        self.data_line4.setData(self.time_5,self.volt1_5)
        self.data_line6.setData(self.time_5,self.curr1_5)

        dplot5 = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        with open(self.PS5_CSM1_csvname, 'a') as csv_file:
            fieldnames = ['DateTime','Time_S', 'Volt1_V', 'Volt2_V', 'Curr1_A', 'Curr2_A']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'DateTime': dplot5, 'Time_S': str(i1_5), 'Volt1_V': str(f1_5), 'Volt2_V': str(f2_5), 'Curr1_A': str(f3_5), 'Curr2_A': str(f4_5)})

        with open(self.PS5_CSM1_txtname, "a") as f:
            #d2 = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
            f.write("%s %s" %(dplot5, "Get IV Data") + '\n')
            f.write("%s %s %s" % (dplot5, "Volt1 (V): ", str(f1_5) +  '\n'))
            f.write("%s %s %s" % (dplot5, "Volt2 (V): ", str(f2_5) + '\n'))
            f.write("%s %s %s" % (dplot5, "Curr1 (A): ", str(f3_5) + '\n'))
            f.write("%s %s %s" % (dplot5, "Curr2 (A): ", str(f4_5) + '\n'))
            f.write("%s %s %s" % (dplot5, "Time (Sec): ", str(i1_5) + '\n'))
            f.close()

        return
        #return self.data_line4, self.data_line5, self.data_line6, self.data_line7
    
    
    #def update_plot_data(self):
    #    if len(self.volt1) > 5:
    #        self.timer.start()
    #        self.volt1 = self.volt1[1:]
    #        self.volt1.append(self.volt1[-1])
    #        print(self.volt1)
    #        self.time = self.time[1:]
    #        self.time.append(self.time[-1] + 1)
    #        print(self.time)
    #        self.graphWidget.clear()
    #        self.data_line.setData(self.time, self.volt1)
    
    def monitor_off(self):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        #self.OFF = PS_off()
        print(self.identifier+"MONITOR OFF")
        #self.result = IV_meas8()
        self.result_5 = IV_meas5()
        #self.label4.setText("%.5f"%(self.result[0]))
        #self.label5.setText("%.5f"%(self.result[1]))
        #self.label6.setText("%.5f"%(self.result[2]))
        #self.label7.setText("%.5f"%(self.result[3]))
        self.label12.setText("%.5f"%(self.result_5[0]))
        self.label13.setText("%.5f"%(self.result_5[1]))
        self.label14.setText("%.5f"%(self.result_5[2]))
        self.label15.setText("%.5f"%(self.result_5[3]))
        #with open(self.PS8_CSM2_txtname, "a") as f:
        #    d3 = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        #    f.write("%s %s" % (d3, "Power Supply OFF") + '\n')
        #    f.close()
        with open(self.PS5_CSM1_txtname, "a") as f:
            doff5time = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
            f.write("%s %s" % (doff5time, "Power Supply OFF") + '\n')
            f.close()
        return 
    
    def update(self):
        #self.label4.adjustSize()
        #self.label5.adjustSize()
        #self.label6.adjustSize()
        #self.label7.adjustSize()
        self.label12.adjustSize()
        self.label13.adjustSize()
        self.label14.adjustSize()
        self.label15.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


