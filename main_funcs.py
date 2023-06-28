#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
from ps_funcs_ps8 import comm8, PS_on8, PS_off8, IV_meas8
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


# In[7]:


class PSWorker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    all_data = pyqtSignal(float, float, float, float, int, object) #v and i data, time data
    GUI_PS = pyqtSignal(float, float, float, float) 


# In[11]:


def __init__(self, MyWindow, identifier):
        super(PSWorker, self).__init__()
        self.MyWindow = MyWindow 
        self.MyWindow.processing = True
        self.identifier = identifier

def run(self):
        self.MyWindow.time_last = 0
        time_accu = self.MyWindow.time_total 
        print(self.identifier + "Start Monitoring")
        start = time.time()
        self.target_time = datetime.datetime.now()
        while self.MyWindow.processing: 
            self.target_time = self.target_time + datetime.timedelta(seconds=60)
            while self.MyWindow.device_release==0:
                pass
            self.MyWindow.device_release=0
            self.data = IV_meas()
            #print("Volt1: " + str(self.data[0][0]))
            #print("Volt2: " + str(self.data[1][0]))
            #print("Curr1: " + str(self.data[2][0]))
            #print("Curr2: " + str(self.data[3][0]))
            #print("Time: " + str(self.target_time))
            #print(type(self.target_time))
            self.MyWindow.device_release = 1
            time.sleep(2)
            end = time.time()                           #Recording and displaying V, I and time for each PS
            self.MyWindow.time_last = end - start 
            #print(type(self.MyWindow.time_last))
            self.GUI_PS.emit(self.data[0][0], self.data[1][0], self.data[2][0], self.data[3][0])
            self.all_data.emit(self.data_ps[0][0], self.data_ps[1][0], self.data_ps[2][0], self.data_ps[3][0], int(self.MyWindow.time_last), self.target_time)
            self.MyWindow.time_total = time_accu + self.MyWindow.time_last 

        print(self.identifier+"End Monitoring")
        print(self.identifier+"Monitoring Time: " + str(end-start))
        self.finished.emit()
        return 


# In[12]:


def stop(self):
        self.MyWindow.processing = False


# In[ ]:


class MyWindowPS(object):
    def __init__(self):
        self.time_total = 0
        self.processing = False
        self.device_release = 1
        self.date_txt = 'BNL'
        self.condition_txt = 'beam_run'
        self.PS_CSM_csvname = 'CSM_' + self.date_txt + '_' + self.condition_txt + '.csv'
        return 


# In[ ]:


def initUI(self, MainWindow, identifier):
        self.volt1 = []
        self.volt2 = []
        self.curr1 = []
        self.curr2 = []
        self.time = []
        self.date = []
        self.identifier = identifier
        
        #TABS
        self.tabWidget = QtWidgets.QTabWidget(MainWindow)
        self.tabWidget.setGeometry(QtCore.QRect(20,20, 300,300))

        self.tab_PS_addr = QtWidgets.QWidget(MainWindow)			#individual tabs for each PS
        self.tabWidget.addTab(self.tab_PS_addr, "PS: ") #address) 
        
        #PRINTOUT LAYOUT
        self.logLayoutWdiget = QtWidgets.QWidget(MainWindow)
        self.logLayoutWdiget.setGeometry(QtCore.QRect(20, 600, 1100, 200))  # (left, top, width, height)
        self.logLayout = QtWidgets.QVBoxLayout(self.logLayoutWdiget)
        self.logLayout.setContentsMargins(0, 0, 0, 0)

        self.label = QtWidgets.QLabel("Run Info", self.logLayoutWdiget)
        self.logLayout.addWidget(self.label)
        self.textBrowser = QtWidgets.QTextBrowser(self.logLayoutWdiget)
        self.logLayout.addWidget(self.textBrowser)
        
        #PS 
        self.layoutWidget = QtWidgets.QWidget(self.tab_PS)
        self.layoutWidget.setGeometry(QtCore.QRect(30,70,200,150))
        self.layout = QtWidgets.QVBoxLayout(self.layoutWidget)

        self.layoutWidget2 = QtWidgets.QWidget(self.tab_PS)
        self.layoutWidget2.setGeometry(QtCore.QRect(150,70,200,150))
        self.layout2 = QtWidgets.QVBoxLayout(self.layoutWidget2)		#adding widgets to layout, buttons?

        self.layoutWidget3 = QtWidgets.QWidget(self.tab_PS)
        self.layoutWidget3.setGeometry(QtCore.QRect(50,-20,200,150))
        self.layout3 = QtWidgets.QVBoxLayout(self.layoutWidget3)		#button b1 - init power supply

        self.layoutWidget4 = QtWidgets.QWidget(self.tab_PS)
        self.layoutWidget4.setGeometry(QtCore.QRect(25,170,130,150))
        self.layout4 = QtWidgets.QVBoxLayout(self.layoutWidget4)		#button b2 - PS ON

        self.layoutWidget5 = QtWidgets.QWidget(self.tab_PS)
        self.layoutWidget5.setGeometry(QtCore.QRect(150,170,130,150))
        self.layout5 = QtWidgets.QVBoxLayout(self.layoutWidget5)		#button b3 - PS OFF
        
        #MONITOR ON/OFF
        self.layoutWidget6 = QtWidgets.QWidget(MainWindow)
        self.layoutWidget6.setGeometry(QtCore.QRect(30,310,150,150))
        self.layout6 = QtWidgets.QVBoxLayout(self.layoutWidget6)

        self.layoutWidget7 = QtWidgets.QWidget(MainWindow)
        self.layoutWidget7.setGeometry(QtCore.QRect(170,310,150,150))
        self.layout7 = QtWidgets.QVBoxLayout(self.layoutWidget7)
        
        #PLOT LAYOUT PS
        self.layoutWidget8 = QtWidgets.QWidget(MainWindow)
        self.layoutWidget8.setGeometry(QtCore.QRect(350, 20, 400, 250))
        self.layout8 = QtWidgets.QHBoxLayout(self.layoutWidget8)

        self.layoutWidget9 = QtWidgets.QWidget(MainWindow)
        self.layoutWidget9.setGeometry(QtCore.QRect(750, 20, 400, 250)) #1050, 20, 370, 250
        self.layout9 = QtWidgets.QHBoxLayout(self.layoutWidget9)
        
        #IV labels PS
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setText("Voltage1 (V):")
        self.layout.addWidget(self.label)

        self.label1 = QtWidgets.QLabel(self.layoutWidget)
        self.label1.setText("Voltage2 (V):")
        self.layout.addWidget(self.label1)					#current and voltage outputs

        self.label2 = QtWidgets.QLabel(self.layoutWidget) 
        self.label2.setText("Current1 (A):")
        self.layout.addWidget(self.label2)

        self.label3 = QtWidgets.QLabel(self.layoutWidget) 
        self.label3.setText("Current2 (A):")
        self.layout.addWidget(self.label3)
        
        #Read IV labels PS
        self.label4 = QtWidgets.QLabel(self.layoutWidget2)
        self.label4.setText("-")
        self.layout2.addWidget(self.label4)

        self.label5 = QtWidgets.QLabel(self.layoutWidget2)
        self.label5.setText("-")
        self.layout2.addWidget(self.label5)

        self.label6 = QtWidgets.QLabel(self.layoutWidget2)
        self.label6.setText("-")
        self.layout2.addWidget(self.label6)

        self.label7 = QtWidgets.QLabel(self.layoutWidget2)
        self.label7.setText("-")
        self.layout2.addWidget(self.label7)
        
        #pushbutton ps
        self.b1 = QtWidgets.QPushButton(self.layoutWidget3)
        self.b1.setText("Init Power Supply")                  
        self.layout3.addWidget(self.b1)
        self.b1.clicked.connect(self.gpib)

        self.b2 = QtWidgets.QPushButton(self.layoutWidget4)
        self.b2.setText("PS ON")            					#PS control buttons
        self.layout4.addWidget(self.b2)
        self.b2.clicked.connect(self.pwr_on)

        self.b3 = QtWidgets.QPushButton(self.layoutWidget5)
        self.b3.setText("PS OFF")
        self.layout5.addWidget(self.b3)
        self.b3.clicked.connect(self.pwr_off)
        self.b3.setEnabled(False)

        self.b4 = QtWidgets.QPushButton(self.layoutWidget6)
        self.b4.setText("MONITOR ON")
        self.layout6.addWidget(self.b4)
        self.b4.clicked.connect(self.monitor_on)
        
        self.b5 = QtWidgets.QPushButton(self.layoutWidget7)
        self.b5.setText("MONITOR OFF")
        self.layout7.addWidget(self.b5)
        self.b5.clicked.connect(self.monitor_off)
        self.b5.setEnabled(False)

        #pyqtgraph
        self.graphWidget = pg.PlotWidget()
        self.pen = pg.mkPen(color="k", width=2)
        self.layout8.addWidget(self.graphWidget)						#voltage and current graphs
        self.graphWidget.setBackground('w')
        self.graphWidget.setTitle("PS Volt1 vs Time (sec)", color="b", size="10pt")
        self.graphWidget.setLabel('left', 'Volt1 (V)', color="r", size="5pt")
        self.graphWidget.setLabel('bottom', 'Time (S)', color="r", size="5pt")
        self.graphWidget.showGrid(x=True, y=True)

        self.data_line =  self.graphWidget.plot(self.time, self.volt1, pen = self.pen)
        
        self.graphWidget2 = pg.PlotWidget()
        self.layout9.addWidget(self.graphWidget2)
        self.graphWidget2.setBackground('w')
        self.graphWidget2.setTitle("PS Curr1 vs Time (sec)", color="b", size="10pt")
        self.graphWidget2.setLabel('left', 'Curr1 (A)', color="r", size="5pt")
        self.graphWidget2.setLabel('bottom', 'Time (S)', color="r", size="5pt")
        self.graphWidget2.showGrid(x=True, y=True)

        self.data_line2 = self.graphWidget2.plot(self.time, self.curr1, pen = self.pen)


# In[ ]:


def gpib(self, addr):								#PS connected to GPIB, comm
      self.gpib_inst = comm('5') #input address?
      print(self.identifier+"Power supply __ connected to GPIB")
      with open(self.PS_CSM_txtname, "a") as f:
          dgpib = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
          f.write("%s %s" % (dgpib, "Power Supply Connected to GPIB") + '\n')
          f.close()
      self.b1.setEnabled(False)


# In[ ]:


def pwr_on(self):
       while self.device_release == 0:
           pass
       self.device_release = 0
       self.ON = PS_on()
       self.device_release = 1
       print(self.identifier+'OUTP ON PS__')
       time.sleep(3)
       with open(self.PS_CSM_txtname, "a") as f:    					#turn on PS
           dop = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
           f.write("%s %s" % (dop, "OUTP ON") + '\n')
           f.close()
       self.b2.setEnabled(False)
       self.b3.setEnabled(True)


# In[ ]:


def pwr_off(self):								#turn off PS 
      while self.device_release == 0:
          pass
      self.device_release = 0
      self.OFF = PS_off()
      self.device_release = 1
      print(self.identifier+'OUTP OFF PS')
      time.sleep(3)
      with open(self.PS_CSM_txtname, "a") as f:
          doff = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
          f.write("%s %s" % (doff, "OUTP OFF") + '\n')
          f.close()
      self.b3.setEnabled(False)
      self.b2.setEnabled(True)


# In[ ]:


def monitor_on(self):							#monitor data
       self.volt1 = []
       self.volt2 = []
       self.curr1 = []
       self.curr2 = []
       self.time = []
       self.date = []

       self.thread = QThread()
       self.worker = PSWorker(self, self.identifier)
       self.worker.moveToThread(self.thread)
       self.thread.started.connect(self.worker.run)
       self.worker.finished.connect(self.thread.quit)
       self.worker.finished.connect(self.worker.deleteLater)
       self.thread.finished.connect(self.thread.deleteLater)
       self.worker.all_data.connect(self.graph)
       #self.worker.all_data_5.connect(self.graph_5)
       self.worker.GUI_PS.connect(self.label_func)
       #self.worker.GUI_PS5.connect(self.label5_func) 
       self.thread.start()
       self.b4.setEnabled(False)
       self.b5.setEnabled(True)
       self.thread.finished.connect(lambda: self.b4.setEnabled(True))
       self.thread.finished.connect(lambda: self.b5.setEnabled(False))
       self.thread.finished.connect(self.monitor_off)
       with open(self.PS_CSM_txtname, "a") as f:
           d1 = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
           f.write("%s %s" %(d1, "Power Supply  ON") + '\n')
           f.close()
       return


# In[ ]:


def label_func(self, par1, par2, par3, par4):
        print("Label GUI PS")
        self.label4.setText("%.5f"%(par1))
        self.label5.setText("%.5f"%(par2))
        self.label6.setText("%.5f"%(par3))
        self.label7.setText("%.5f"%(par4))
        print(self.identifier+"PS Volt1: "+"%.5f"%(par1))
        print(self.identifier+"PS Volt2: "+"%.5f"%(par2))
        print(self.identifier+"PS Curr1: "+"%.5f"%(par3))
        print(self.identifier+"PS Curr2: "+"%.5f"%(par4))
        return par1, par2, par3, par4


# In[ ]:


def graph(self, f1, f2, f3, f4, i1, obj1):
     print("Get PS Data")
     self.volt1.append(f1)
     self.volt2.append(f2)
     self.curr1.append(f3)
     self.curr2.append(f4)
     self.time.append(i1)
     self.date.append(obj1)

     if len(self.time) > 30:
         self.volt1 = self.volt1[1:]
         self.volt2 = self.volt2[1:]
         self.curr1 = self.curr1[1:] 
         self.curr2 = self.curr2[1:]
         self.time = self.time[1:] 
         self.date = self.date[1:] 
     '''
     self.data_line =  self.graphWidget.plot(self.time, self.volt1, pen = self.pen)
     #self.data_line1 = self.graphWidget1.plot(self.time, self.volt2, pen = self.pen)
     self.data_line2 = self.graphWidget2.plot(self.time, self.curr1, pen = self.pen)
     #self.data_line3 = self.graphWidget3.plot(self.time, self.curr2, pen = self.pen)
     '''

     self.data_line.setData(self.time,self.volt1)
     self.data_line2.setData(self.time,self.curr1)

     d2 = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
     with open(self.PS_CSM_csvname, 'a') as csv_file:
         fieldnames = ['DateTime','Time_S', 'Volt1_V', 'Volt2_V', 'Curr1_A', 'Curr2_A']
         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

         writer.writeheader()
         writer.writerow({'DateTime': d2, 'Time_S': str(i1), 'Volt1_V': str(f1), 'Volt2_V': str(f2), 'Curr1_A': str(f3), 'Curr2_A': str(f4)})

     with open(self.PS_CSM_txtname, "a") as f:
         #d2 = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
         f.write("%s %s" %(d2, "Get IV Data") + '\n')
         f.write("%s %s %s" % (d2, "Volt1 (V): ", str(f1) +  '\n'))
         f.write("%s %s %s" % (d2, "Volt2 (V): ", str(f2) + '\n'))
         f.write("%s %s %s" % (d2, "Curr1 (A): ", str(f3) + '\n'))
         f.write("%s %s %s" % (d2, "Curr2 (A): ", str(f4) + '\n'))
         f.write("%s %s %s" % (d2, "Time (Sec): ", str(i1) + '\n'))
         #f.write("%s %s %s" % (d2, "Date: ", str(obj1) + '\n' ))
         f.close()

     return


# In[ ]:


def monitor_off(self):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        #self.OFF = PS_off()
        print(self.identifier+"MONITOR OFF")
        self.result = IV_meas()
        self.label4.setText("%.5f"%(self.result[0]))
        self.label5.setText("%.5f"%(self.result[1]))
        self.label6.setText("%.5f"%(self.result[2]))
        self.label7.setText("%.5f"%(self.result[3]))    						#monitor off
        with open(self.PS_CSM_txtname, "a") as f:
            d3 = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
            f.write("%s %s" % (d3, "Power Supply OFF") + '\n')
            f.close()
        return 


# In[ ]:


def update(self):
       self.label4.adjustSize()
       self.label5.adjustSize()
       self.label6.adjustSize()
       self.label7.adjustSize()


# In[ ]:


def window():
    app = QApplication(sys.argv)
#     num_ps = input("Number of Power Supplies: ")
#     for i in range (num_ps):
#         ps_address = input("PS Address: ")
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())      

