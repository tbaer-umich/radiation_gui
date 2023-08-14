#!/usr/bin/env python
# coding: utf-8

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
from ps_funcs import *
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
from functools import partial

class PSWorker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    all_data = pyqtSignal(float, float, float, float, int, object)
    GUI_PS = pyqtSignal(float, float, float, float)


    def __init__(self, MyWindow, identifier):
            super(PSWorker, self).__init__()
            self.MyWindow = MyWindow 
            self.MyWindow.processing = True
            self.identifier = identifier
            '''
            self.all_data = {}
            self.GUI_ps = {}
            for i in range (int (self.ps_num)):
                self.all_data["All Data {0}".format(i)] = pyqtSignal(float, float, float, float, int, object) #v and i data, time data
                self.GUI_ps["GUI PS {0}".format(i)] = pyqtSignal(float, float, float, float)
            '''
    def run(self,addr, volt1, curr1, volt2, curr2):
        self.MyWindow.time_last = 0
        time_accu = self.MyWindow.time_total 
        print(self.identifier +  "Start Monitoring")
        start = time.time()
        self.target_time = datetime.datetime.now()
        while self.MyWindow.processing:
            self.target_time = self.target_time + datetime.timedelta(seconds=60)
            while self.MyWindow.device_release==0:
                pass
            self.MyWindow.device_release=0
            
            self.data = IV_meas(addr, volt1, curr1, volt2, curr2)
            self.MyWindow.device_release = 1
            time.sleep(2)
            end = time.time()                           #Recording and displaying V, I and time for each PS
            self.MyWindow.time_last = end - start 
            #print(type(self.MyWindow.time_last))
            self.GUI_PS.emit(self.data[0][0], self.data[1][0], self.data[2][0], self.data[3][0])
            self.all_data.emit(self.data[0][0], self.data[1][0], self.data[2][0], self.data[3][0], int(self.MyWindow.time_last), self.target_time)
            
            self.MyWindow.time_total = time_accu + self.MyWindow.time_last

        print(self.identifier+"End Monitoring")
        print(self.identifier+"Monitoring Time: " + str(end-start))
        
        self.finished.emit()
             

    def stop(self):
            self.MyWindow.processing = False

class MyWindowPS(object):
    def __init__(self):
        self.time_total = 0
        self.processing = False
        self.device_release = 1
        self.date_txt = 'BNL'
        self.condition_txt = 'beam_run'
        self.ps_num = input("How many PS? ")
        self.csv_file = {}
        self.txt_file = {}
        self.PS_CSM_csvname = 'CSM_' + self.date_txt + '_' + self.condition_txt + '.csv'
        self.PS_CSM_txtname = 'CSM_' + self.date_txt + '_' + self.condition_txt + '.txt'
       # for i in range (int(self.ps_num)):
       #     self.csv_file["CSV{0}".format(i)] = 'CSM_' + str(i)  + self.date_txt + '_' + self.condition_txt + '.csv'
       #     self.txt_file["TXT{0}".format(i)] = 'CSM_' + str(i)  + self.date_txt + '_' + self.condition_txt + '.txt'
        return 


# In[ ]:


    def initUI(self, MainWindow, identifier):
            self.volt1 = []
            self.curr1 = []
            self.time = []
            self.date = []
            self.identifier = identifier
            
            self.addr = {}
            self.voltage1 = {}
            self.current1 = {}
            self.voltage2 = {}
            self.current2 = {}
            self.volt1_data = {}
            self.curr1_data = {}
            self.volt2_data = {}
            self.curr2_data = {}
            self.dict_PSON = {}
            self.dict_PSOFF = {}
            self.dict_PS_init = {}
            self.layoutWidget = {}
            self.layout = {}
            self.layoutWidget2 = {}
            self.layout2 = {}
            self.dict_PSINIT_layout = {}
            self.dict_PSON_layout = {}
            self.dict_PSOFF_layout = {}
            self.dict_v = {}
            self.dict_c = {}
            self.dict_v2 = {}
            self.dict_c2 = {}
            self.dict_dash_v = {}
            self.dict_dash_c = {}
            self.dict_dash_v2 = {}
            self.dict_dash_c2 = {}
            self.dict_init_button = {}
            self.dict_on_button = {}
            self.dict_off_button = {}
            self.dict_plot_layout = {}
            self.dict_ps_layout = {}
            self.dict_plot_layout2 = {}
            self.dict_ps_layout2 = {}
            self.dict_PStabs = {}
            self.dict_graph_widget = {}
            self.dict_graph_widget2 = {}
            self.volt1_data_line = {}
            self.curr1_data_line = {}
            self.volt2_data_line = {}
            self.curr2_data_line = {}
            self.monitor_on_button = {}
            self.monitor_off_button = {}
            self.monitor_on_widget = {}
            self.monitor_off_widget = {}
            self.monitor_on_layout = {}
            self.monitor_off_layout = {}
            self.address_widget = {}
            self.address_layout = {}
            self.address_label = {}
            self.addr_num_widget = {}
            self.addr_num_layout = {}
            self.addr_num_label = {}
            self.tabwidget = {}

            #TABS
            self.tabWidget = QtWidgets.QTabWidget(MainWindow)
            self.tabWidget.setGeometry(QtCore.QRect(20,20, 1100,650))

            #PRINTOUT LAYOUT
            self.logLayoutWdiget = QtWidgets.QWidget(MainWindow)
            self.logLayoutWdiget.setGeometry(QtCore.QRect(20, 680, 1100, 200))  # (left, top, width, height)
            self.logLayout = QtWidgets.QVBoxLayout(self.logLayoutWdiget)
            self.logLayout.setContentsMargins(0, 0, 0, 0)

            self.label = QtWidgets.QLabel("Run Info", self.logLayoutWdiget)
            self.logLayout.addWidget(self.label)
            self.textBrowser = QtWidgets.QTextBrowser(self.logLayoutWdiget)
            self.logLayout.addWidget(self.textBrowser)
            
            '''
            try:
                n = int(self.ps_num)
            except ValueError:
                print ("Only numbers are accepted. Please enter a number.")
            '''

            self.addr_list = []
            self.voltage_list = []
            self.current_list = []

            self.volt1_dict = {}
            self.volt2_dict = {}
            self.curr1_dict = {}
            self.curr2_dict = {}

            for i in range (int(self.ps_num)):

                self.volt1_data["Output 1 Volt{0}".format(i)] = []
                self.curr1_data["Output 1 Curr{0}".format(i)] = []
                self.volt2_data["Output 2 Volt{0}".format(i)] = []
                self.curr2_data["Output 2 Curr{0}".format(i)] = []
                
                self.addr["Address{0}".format(i)] = int(input("Address for PS" + str(i) + ": "))
                self.addr_list.append(self.addr["Address{0}".format(i)])

                self.voltage1["Voltage{0}".format(i)] = int(input("Max Voltage for PS" + str(i) + " Output 1: "))

                self.current1["Current{0}".format(i)] = int(input("Max Current for PS" + str(i) + " Output 1: "))
                
                self.voltage2["Voltage{0}".format(i)] = int(input("Max Voltage for PS" + str(i) + " Output 2: "))

                self.current2["Current{0}".format(i)] = int(input("Max Current for PS" + str(i) + " Output 2: "))
                
                self.dict_PStabs["PS{0}".format(i)] = QtWidgets.QWidget(MainWindow)
                self.tabWidget.addTab(self.dict_PStabs["PS{0}".format(i)], "PS" + str(i))

                self.layoutWidget["FirstLayout{0}".format(i)] = QtWidgets.QWidget( self.dict_PStabs["PS{0}".format(i)])
                self.layoutWidget["FirstLayout{0}".format(i)].setGeometry(QtCore.QRect(30,70,200,150))
                self.layout["Layout{0}".format(i)] = QtWidgets.QVBoxLayout(self.layoutWidget["FirstLayout{0}".format(i)])

                self.layoutWidget2["SecondLayout{0}".format(i)] = QtWidgets.QWidget( self.dict_PStabs["PS{0}".format(i)])
                self.layoutWidget2["SecondLayout{0}".format(i)].setGeometry(QtCore.QRect(150,70,200,150))
                self.layout2["Layout{0}".format(i)] = QtWidgets.QVBoxLayout(self.layoutWidget2["SecondLayout{0}".format(i)])

                self.dict_PS_init["INIT PS{0}".format(i)] = QtWidgets.QWidget( self.dict_PStabs["PS{0}".format(i)])
                self.dict_PS_init["INIT PS{0}".format(i)].setGeometry(QtCore.QRect(60,-20,200,150))
                self.dict_PSINIT_layout["PS{0} Layout".format(i)] = QtWidgets.QVBoxLayout(self.dict_PS_init["INIT PS{0}".format(i)])

                self.dict_init_button["Init button PS{0}".format(i)] = QtWidgets.QPushButton(  self.dict_PS_init["INIT PS{0}".format(i)])
                self.dict_init_button["Init button PS{0}".format(i)].setText("Init Power Supply " + str(i))
                self.dict_PSINIT_layout["PS{0} Layout".format(i)].addWidget( self.dict_init_button["Init button PS{0}".format(i)])
                self.dict_init_button["Init button PS{0}".format(i)].clicked.connect(lambda:self.gpib(int(self.addr_list[i]),int(i),self.voltage1["Voltage{0}".format(i)],self.current1["Current{0}".format(i)],self.voltage2["Voltage{0}".format(i)],self.current2["Current{0}".format(i)]))

                self.dict_PSON["PS{0} ON".format(i)] = QtWidgets.QWidget(self.dict_PStabs["PS{0}".format(i)])
                self.dict_PSON["PS{0} ON".format(i)].setGeometry(QtCore.QRect(25,170,130,150))
                self.dict_PSON_layout["PS{0} Layout".format(i)] = QtWidgets.QVBoxLayout(self.dict_PSON["PS{0} ON".format(i)])

                self.dict_on_button["PS{0} On button".format(i)] = QtWidgets.QPushButton(self.dict_PSON["PS{0} ON".format(i)])
                self.dict_on_button["PS{0} On button".format(i)].setText("PS " + str(i) + " ON")
                self.dict_PSON_layout["PS{0} Layout".format(i)].addWidget(self.dict_on_button["PS{0} On button".format(i)] )
                self.dict_on_button["PS{0} On button".format(i)].clicked.connect(lambda:self.pwr_on(int(self.addr_list[i]),int(i),self.voltage1["Voltage{0}".format(i)],self.current1["Current{0}".format(i)]    ,self.voltage2["Voltage{0}".format(i)],self.current2["Current{0}".format(i)] ))

                self.dict_PSOFF["PS{0} OFF".format(i)] = QtWidgets.QWidget(self.dict_PStabs["PS{0}".format(i)])
                self.dict_PSOFF["PS{0} OFF".format(i)].setGeometry(QtCore.QRect(150,170,130,150))
                self.dict_PSOFF_layout["PS{0} Layout".format(i)] = QtWidgets.QVBoxLayout(self.dict_PSOFF["PS{0} OFF".format(i)])

                self.dict_off_button["PS{0} Off button".format(i)] = QtWidgets.QPushButton(self.dict_PSOFF["PS{0} OFF".format(i)])
                self.dict_off_button["PS{0} Off button".format(i)].setText("PS " + str(i) + " OFF")
                self.dict_PSOFF_layout["PS{0} Layout".format(i)].addWidget(self.dict_off_button["PS{0} Off button".format(i)] )
                self.dict_off_button["PS{0} Off button".format(i)].clicked.connect(lambda:self.pwr_off(int(self.addr_list[i]),int(i),self.voltage1["Voltage{0}".format(i)],self.current1["Current{0}".format(i)]    ,self.voltage2["Voltage{0}".format(i)],self.current2["Current{0}".format(i)] ))

                self.dict_v["PS{0} Voltage1".format(i)] = QtWidgets.QLabel(self.layoutWidget["FirstLayout{0}".format(i)])
                self.dict_v["PS{0} Voltage1".format(i)].setText(str ("PS" + str (i) + " Voltage 1:"))
                self.layout["Layout{0}".format(i)].addWidget(self.dict_v["PS{0} Voltage1".format(i)])

                self.dict_v2["PS{0} Voltage2".format(i)] = QtWidgets.QLabel(self.layoutWidget["FirstLayout{0}".format(i)])
                self.dict_v2["PS{0} Voltage2".format(i)].setText(str ("PS" + str (i) + " Voltage 2:"))
                self.layout["Layout{0}".format(i)].addWidget(self.dict_v2["PS{0} Voltage2".format(i)])
                
                self.dict_c["PS{0} Current".format(i)] = QtWidgets.QLabel(self.layoutWidget["FirstLayout{0}".format(i)])
                self.dict_c["PS{0} Current".format(i)].setText(str ("PS" + str (i) + " Current 1:"))
                self.layout["Layout{0}".format(i)].addWidget(self.dict_c["PS{0} Current".format(i)])

                self.dict_c2["PS{0} Current2".format(i)] = QtWidgets.QLabel(self.layoutWidget["FirstLayout{0}".format(i)])
                self.dict_c2["PS{0} Current2".format(i)].setText(str ("PS" + str (i) + " Current 2:"))
                self.layout["Layout{0}".format(i)].addWidget(self.dict_c2["PS{0} Current2".format(i)])
                
                self.dict_dash_v["PS{0} Dash".format(i)] = QtWidgets.QLabel(self.layoutWidget2["SecondLayout{0}".format(i)])
                self.dict_dash_v["PS{0} Dash".format(i)].setText("-")
                self.layout2["Layout{0}".format(i)].addWidget(self.dict_dash_v["PS{0} Dash".format(i)])

                self.dict_dash_v2["PS{0} Dash".format(i)] = QtWidgets.QLabel(self.layoutWidget2["SecondLayout{0}".format(i)])
                self.dict_dash_v2["PS{0} Dash".format(i)].setText("-")
                self.layout2["Layout{0}".format(i)].addWidget(self.dict_dash_v2["PS{0} Dash".format(i)])

                self.dict_dash_c["PS{0} Dash".format(i)] = QtWidgets.QLabel(self.layoutWidget2["SecondLayout{0}".format(i)])
                self.dict_dash_c["PS{0} Dash".format(i)].setText("-")
                self.layout2["Layout{0}".format(i)].addWidget(self.dict_dash_c["PS{0} Dash".format(i)])

                self.dict_dash_c2["PS{0} Dash".format(i)] = QtWidgets.QLabel(self.layoutWidget2["SecondLayout{0}".format(i)])
                self.dict_dash_c2["PS{0} Dash".format(i)].setText("-")
                self.layout2["Layout{0}".format(i)].addWidget(self.dict_dash_c2["PS{0} Dash".format(i)])
                
                self.monitor_on_widget["Monitor on{0}".format(i)] = QtWidgets.QWidget(self.dict_PStabs["PS{0}".format(i)])
                self.monitor_on_widget["Monitor on{0}".format(i)].setGeometry(QtCore.QRect(25,240,130,150))
                self.monitor_on_layout["Monitor on{0}".format(i)] = QtWidgets.QVBoxLayout(self.monitor_on_widget["Monitor on{0}".format(i)])

                self.monitor_off_widget["Monitor off{0}".format(i)] = QtWidgets.QWidget(self.dict_PStabs["PS{0}".format(i)])
                self.monitor_off_widget["Monitor off{0}".format(i)].setGeometry(QtCore.QRect(150,240,130,150))
                self.monitor_off_layout["Monitor off{0}".format(i)] = QtWidgets.QVBoxLayout(self.monitor_off_widget["Monitor off{0}".format(i)])

                self.monitor_on_button["Monitor on{0}".format(i)] = QtWidgets.QPushButton(self.monitor_on_widget["Monitor on{0}".format(i)])
                self.monitor_on_button["Monitor on{0}".format(i)].setText("MONITOR ON")
                self.monitor_on_layout["Monitor on{0}".format(i)].addWidget(self.monitor_on_button["Monitor on{0}".format(i)])
                self.monitor_on_button["Monitor on{0}".format(i)].clicked.connect(lambda: self.monitor_on(int(i)))

                self.monitor_off_button["Monitor off{0}".format(i)] = QtWidgets.QPushButton(self.monitor_off_widget["Monitor off{0}".format(i)])
                self.monitor_off_button["Monitor off{0}".format(i)].setText("MONITOR OFF")
                self.monitor_off_layout["Monitor off{0}".format(i)].addWidget(self.monitor_off_button["Monitor off{0}".format(i)])
                self.monitor_off_button["Monitor off{0}".format(i)].clicked.connect(lambda: self.monitor_off(int(i)))
                self.monitor_off_button["Monitor off{0}".format(i)].setEnabled(False)
                               
                self.address_widget["Address Widget{0}".format(i)] = QtWidgets.QWidget(self.dict_PStabs["PS{0}".format(i)])
                self.address_widget["Address Widget{0}".format(i)].setGeometry(QtCore.QRect(20,530,150,150))
                self.address_layout["Address layout{0}".format(i)] = QtWidgets.QVBoxLayout(self.address_widget["Address Widget{0}".format(i)])

                self.address_label["Address Label{0}".format(i)] = QtWidgets.QLabel(self.address_widget["Address Widget{0}".format(i)])
                self.address_label["Address Label{0}".format(i)].setText("PS" + str(i) + " Address: ")
                self.address_layout["Address layout{0}".format(i)].addWidget(self.address_label["Address Label{0}".format(i)])

                self.addr_num_widget["Address Widget{0}".format(i)] = QtWidgets.QWidget(self.dict_PStabs["PS{0}".format(i)])
                self.addr_num_widget["Address Widget{0}".format(i)].setGeometry(QtCore.QRect(130,530,150,150))
                self.addr_num_layout["Address layout{0}".format(i)] = QtWidgets.QVBoxLayout(self.addr_num_widget["Address Widget{0}".format(i)])

                self.addr_num_label["Address Label{0}".format(i)] = QtWidgets.QLabel(self.addr_num_widget["Address Widget{0}".format(i)])
                self.addr_num_label["Address Label{0}".format(i)].setText(str(self.addr_list[i]))
                self.addr_num_layout["Address layout{0}".format(i)].addWidget(self.addr_num_label["Address Label{0}".format(i)])

                self.dict_plot_layout["PS{0} plot layout".format(i)] = QtWidgets.QWidget(self.dict_PStabs["PS{0}".format(i)])
                self.dict_plot_layout["PS{0} plot layout".format(i)].setGeometry(QtCore.QRect(500, 0, 500, 300))
                self.dict_ps_layout["PS{0} plot layout".format(i)] = QtWidgets.QHBoxLayout(self.dict_plot_layout["PS{0} plot layout".format(i)])
               
                self.dict_graph_widget["PS{0} plot layout".format(i)] = pg.PlotWidget()
                self.pen = pg.mkPen(color="k", width=2)
                self.pen2 = pg.mkPen(color="r", width=2)
                self.dict_ps_layout["PS{0} plot layout".format(i)].addWidget(self.dict_graph_widget["PS{0} plot layout".format(i)])
                self.dict_graph_widget["PS{0} plot layout".format(i)].setBackground('w')
                self.dict_graph_widget["PS{0} plot layout".format(i)].setTitle("PS" + str(i) +  " Voltage vs Time (sec)", color="k", size="12pt")
                self.dict_graph_widget["PS{0} plot layout".format(i)].setLabel('left', 'Voltage (V)', color="r", size="5pt")
                self.dict_graph_widget["PS{0} plot layout".format(i)].setLabel('bottom', 'Time (S)', color="r", size="5pt")
                self.dict_graph_widget["PS{0} plot layout".format(i)].showGrid(x=True, y=True)
                
                self.dict_graph_widget["PS{0} plot layout".format(i)].addLegend()

                self.volt1_data_line["PS{0} Voltage1 Data Line".format(i)] =  self.dict_graph_widget["PS{0} plot layout".format(i)].plot(self.time, self.volt1_data["Output 1 Volt{0}".format(i)], pen = self.pen, name = "Output 1 Voltage")
                self.volt2_data_line["PS{0} Voltage2 Data Line".format(i)] =  self.dict_graph_widget["PS{0} plot layout".format(i)].plot(self.time, self.volt2_data["Output 2 Volt{0}".format(i)], pen = self.pen2, name = "Output 2 Voltage")

                self.dict_plot_layout2["PS{0} plot layout".format(i)] = QtWidgets.QWidget(self.dict_PStabs["PS{0}".format(i)])
                self.dict_plot_layout2["PS{0} plot layout".format(i)].setGeometry(QtCore.QRect(500, 300, 500, 300))
                self.dict_ps_layout2["PS{0} plot layout".format(i)] = QtWidgets.QHBoxLayout(self.dict_plot_layout2["PS{0} plot layout".format(i)])
                
                self.pen3 = pg.mkPen(color="k",width=2)
                self.pen4 = pg.mkPen(color="r",width=2)
                self.dict_graph_widget2["PS{0} plot layout".format(i)] = pg.PlotWidget()
                self.dict_ps_layout2["PS{0} plot layout".format(i)].addWidget(self.dict_graph_widget2["PS{0} plot layout".format(i)])
                self.dict_graph_widget2["PS{0} plot layout".format(i)].setBackground('w')
                self.dict_graph_widget2["PS{0} plot layout".format(i)].setTitle("PS" + str(i) +  " Current vs Time (sec)", color="k", size="12pt")
                self.dict_graph_widget2["PS{0} plot layout".format(i)].setLabel('left', 'Current (A)', color="r", size="5pt")
                self.dict_graph_widget2["PS{0} plot layout".format(i)].setLabel('bottom', 'Time (S)', color="r", size="5pt")
                self.dict_graph_widget2["PS{0} plot layout".format(i)].showGrid(x=True, y=True)

                self.dict_graph_widget2["PS{0} plot layout".format(i)].addLegend()

                self.curr1_data_line["PS{0} Current1  Data Line".format(i)] = self.dict_graph_widget2["PS{0} plot layout".format(i)].plot(self.time, self.curr1_data["Output 1 Curr{0}".format(i)], pen = self.pen3, name = "Output 1 Current")
                self.curr2_data_line["PS{0} Current2  Data Line".format(i)] = self.dict_graph_widget2["PS{0} plot layout".format(i)].plot(self.time, self.curr2_data["Output 2 Curr{0}".format(i)], pen = self.pen4, name = "Output 2 Current")
           # print (self.identifier , self.volt1_dict)
    def print_str(self,string):
        print(string)

    def gpib(self,addr,j, volt1, curr1, volt2, curr2):	#PS connected to GPIB, comm
          print (self.identifier + "here")
          print (self.identifier + str( volt1 ) + str(curr1) + str(volt2) + str(curr2))
          self.gpib_inst = comm(addr, volt1, curr1, volt2, curr2) #with user input, should be comm(addr)
          print(self.identifier+"Power supply " + str(j) + " connected to GPIB")
          with open(self.PS_CSM_txtname, "a") as f:
              dgpib = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
              f.write("%s %s" % (dgpib, "Power Supply Connected to GPIB") + '\n')
              f.close()
          print ("PS" + str(j) + " has address " + str( addr))
          self.dict_init_button["Init button PS{0}".format(j)].setEnabled(False)
          

    def pwr_on(self,addr,j, volt1, curr1, volt2, curr2):
           while self.device_release == 0:
               pass
           self.device_release = 0
           self.ON = PS_on(addr, volt1, curr1, volt2, curr2)
           self.device_release = 1
           print(self.identifier+'OUTP ON PS__')
           time.sleep(3)
           with open(self.PS_CSM_txtname, "a") as f:    					#turn on PS
               dop = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
               f.write("%s %s" % (dop, "OUTP ON") + '\n')
               f.close()
           self.dict_on_button["PS{0} On button".format(j)].setEnabled(False)
           self.dict_off_button["PS{0} Off button".format(j)].setEnabled(True)

    def pwr_off(self,addr,j, volt1, curr1, volt2, curr2):								#turn off PS 
          while self.device_release == 0:
              pass
          self.device_release = 0
          self.OFF = PS_off(addr, volt1, curr1, volt2, curr2)
          self.device_release = 1
          print(self.identifier+'OUTP OFF PS')
          time.sleep(3)
          with open(self.PS_CSM_txtname, "a") as f:
              doff = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
              f.write("%s %s" % (doff, "OUTP OFF") + '\n')
              f.close()
          self.dict_off_button["PS{0} Off button".format(j)].setEnabled(False)
          self.dict_on_button["PS{0} On button".format(j)].setEnabled(True)

    def monitor_on(self,i):
        
        self.volt1_data["Output 1 Volt{0}".format(i)] = []
        self.curr1_data["Output 1 Curr{0}".format(i)] = []
        self.volt2_data["Output 2 Volt{0}".format(i)] = []
        self.curr2_data["Output 2 Curr{0}".format(i)] = []
        
        self.thread = QThread()                                          
        self.worker = PSWorker(self, self.identifier)
        
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(partial(self.worker.run, int(self.addr_list[i]),self.voltage1["Voltage{0}".format(i)],self.current1["Current{0}".format(i)]    ,self.voltage2["Voltage{0}".format(i)],self.current2["Current{0}".format(i)] ))
        
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)            
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.all_data.connect(partial(self.graph, int(i)))
        self.worker.GUI_PS.connect(partial(self.label_func, int(i)))
        self.thread.start()
        self.monitor_on_button["Monitor on{0}".format(i)].setEnabled(False)
        self.monitor_off_button["Monitor off{0}".format(i)].setEnabled(True)
        self.thread.finished.connect(lambda: self.monitor_on_button["Monitor on{0}".format(i)].setEnabled(True))
        self.thread.finished.connect(lambda: self.monitor_off_button["Monitor off{0}".format(i)].setEnabled(False))
        self.thread.finished.connect(lambda: self.monitor_off(int (i)))
        '''
        with open(self.PS_CSM_txtname, "a") as f:
            d = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
            f.write("%s %s" %(d, "Power Supply  ON") + '\n')
            f.close()
            '''
        return

    def label_func(self, i, par1, par2, par3, par4):
            print("Label GUI PS")
            self.dict_dash_v["PS{0} Dash".format(i)].setText("%.5f"%(par1))
            self.dict_dash_v2["PS{0} Dash".format(i)].setText("%.5f"%(par2))
            self.dict_dash_c["PS{0} Dash".format(i)].setText("%.5f"%(par3))
            self.dict_dash_c2["PS{0} Dash".format(i)].setText("%.5f"%(par4))
            print(self.identifier+"PS" + str(i) + " Volt1: "+"%.5f"%(par1))
            print(self.identifier+"PS" + str(i) + " Volt2: "+"%.5f"%(par2))
            print(self.identifier+"PS" + str(i) + " Curr1: "+"%.5f"%(par3))
            print(self.identifier+"PS" + str(i) + " Curr2: "+"%.5f"%(par4))
            return par1, par2, par3, par4

    def graph(self, i, f1, f2, f3, f4, i1, obj1):
         print("Get PS Data")
         self.volt1_data["Output 1 Volt{0}".format(i)].append(f1)
         self.volt2_data["Output 2 Volt{0}".format(i)].append(f2)
         self.curr1_data["Output 1 Curr{0}".format(i)].append(f3)
         self.curr2_data["Output 2 Curr{0}".format(i)].append(f4)           #need separate time and date dictionaries?
         self.time.append(i1)
         self.date.append(obj1)

         if len(self.time) > 30:
             self.volt1_data["Output 1 Volt{0}".format(i)] = self.volt1_data["Output 1 Volt{0}".format(i)][1:]
             self.volt2_data["Output 2 Volt{0}".format(i)] = self.volt2_data["Output 2 Volt{0}".format(i)][1:]
             self.curr1_data["Output 1 Curr{0}".format(i)] = self.curr1_data["Output 1 Curr{0}".format(i)][1:] 
             self.curr2_data["Output 2 Curr{0}".format(i)] = self.curr2_data["Output 2 Curr{0}".format(i)][1:]
             self.time = self.time[1:] 
             self.date = self.date[1:] 

         self.volt1_data_line["PS{0} Voltage1 Data Line".format(i)].setData(self.time,self.volt1_data["Output 1 Volt{0}".format(i)])
         self.volt2_data_line["PS{0} Voltage2 Data Line".format(i)].setData(self.time,self.volt2_data["Output 2 Volt{0}".format(i)])
         self.curr1_data_line["PS{0} Current1  Data Line".format(i)].setData(self.time,self.curr1_data["Output 1 Curr{0}".format(i)])
         self.curr2_data_line["PS{0} Current2  Data Line".format(i)].setData(self.time,self.curr2_data["Output 2 Curr{0}".format(i)])

         d2 = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
         with open(self.PS_CSM_csvname, 'a') as csv_file:
             fieldnames = ['DateTime','Time_S', 'Volt1_V PS'+str(i) , 'Volt2_V PS'+str(i), 'Curr1_A PS'+str(i), 'Curr2_A PS'+str(i)]
             writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

             writer.writeheader()
             writer.writerow({'DateTime': d2, 'Time_S': str(i1), 'Volt1_V PS'+str(i): str(f1), 'Volt2_V PS'+str(i): str(f2), 'Curr1_A PS'+str(i): str(f3), 'Curr2_A PS'+str(i                                                                                                                                                                   ): str(f4)})

         with open(self.PS_CSM_txtname, "a") as f:
             #d2 = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
             f.write("%s %s" %(d2, "Get IV Data") + '\n')
             f.write("%s %s %s" % (d2, "Volt1 PS" + str(i)+" (V): ", str(f1) +  '\n'))
             f.write("%s %s %s" % (d2, "Volt2 PS" + str(i)+" (V): ", str(f2) + '\n'))
             f.write("%s %s %s" % (d2, "Curr1 PS" + str(i)+" (A): ", str(f3) + '\n'))
             f.write("%s %s %s" % (d2, "Curr2 PS" + str(i)+" (A): ", str(f4) + '\n'))
             f.write("%s %s %s" % (d2, "Time (Sec): ", str(i1) + '\n'))
             #f.write("%s %s %s" % (d2, "Date: ", str(obj1) + '\n' ))
             f.close()

         return

    def monitor_off(self,i):
            self.IV_off = {}
            self.worker.stop()
            self.thread.quit()
            self.thread.wait()
            #self.OFF = PS_off()
            print(self.identifier+"MONITOR OFF")
            self.IV_off["PS{0} IV off".format(i)] = IV_meas(int(self.addr_list[i]),self.voltage1["Voltage{0}".format(i)],self.current1["Current{0}".format(i)]    ,self.voltage2["Voltage{0}".format(i)],self.current2["Current{0}".format(i)])
            self.dict_dash_v["PS{0} Dash".format(i)].setText("%.5f"%(self.IV_off["PS{0} IV off".format(i)][0]))
            self.dict_dash_v2["PS{0} Dash".format(i)].setText("%.5f"%( self.IV_off["PS{0} IV off".format(i)][1]))
            self.dict_dash_c["PS{0} Dash".format(i)].setText("%.5f"%( self.IV_off["PS{0} IV off".format(i)][2]))
            self.dict_dash_c2["PS{0} Dash".format(i)].setText("%.5f"%( self.IV_off["PS{0} IV off".format(i)][3]))    						#monitor off
            with open(self.PS_CSM_txtname, "a") as f:
                d3 = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
                f.write("%s %s" % (d3, "Power Supply OFF") + '\n')
                f.close()
            return 

    def update(self):
           self.dict_dash_v["PS{0} Dash".format(i)].adjustSize()
           self.dict_dash_v2["PS{0} Dash".format(i)].adjustSize()
           self.dict_dash_c["PS{0} Dash".format(i)].adjustSize()
           self.dict_dash_c2["PS{0} Dash".format(i)].adjustSize()

    def window():
        app = QApplication(sys.argv)
        win = MyWindow()
        win.show()
        sys.exit(app.exec_())      

