#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pyvisa 
import time 
import sys 
import os 
import scanf


# In[38]:


def comm(addr):                               #establish connection with GPIB with resource manager for PS
    addr = int(addr) #turn argument into integer
    rm = pyvisa.ResourceManager() #define resource 
    resource = rm.list_resources() # Returns a tuple of all connected devices matching query
    gpib_inst = rm.open_resource('GPIB0::{}::INSTR'.format(addr)) #access resource manager for gpib, create insturment object

    for i in range(1,3):
        inst = gpib_inst.write('INST:SEL OUT{}'.format(i))

        instq = gpib_inst.query('INST:SEL?') 
        
        appl = gpib_inst.write('APPL 7.0, 2.0')
#         v_applied = input("Maximum Voltage: ")
#         i_applied = input ("Maximum Current: ")
#         appl = gpib_inst.write('Voltage: ', v_applied, 'Current: ', i_applied) #apply current and voltage values and check, ask for user input
        
        applq = gpib_inst.query('APPL?')
 
    return gpib_inst


# In[39]:


def PS_on():                                   #power on 
    gpib_inst = comm('5') #global address here 
    for i in range(1,3):
        outp = gpib_inst.write('INST:SEL OUT{}'.format(i))
        outpq = gpib_inst.query('INST:SEL?')
        outp_on = gpib_inst.write('OUTP ON')
        outp_onq = gpib_inst.query('OUTP?')
        #print('INST:SEL: ', outpq, 'OUTP: ', outp_onq)
    
    time.sleep(2)
    #Include timer 
    #Log File: Power Supply Output ON 

#PS_on()


# In[40]:


def PS_off():                                   #power off 
    gpib_inst = comm('5')
    outp_off = gpib_inst.write('OUTP OFF')
    outp_offq = gpib_inst.query('OUTP?')
    #print('OUTP: ', outp_offq)

    #Include timer 
    #Log File: Power Supply Output Off 

#PS_off()


# In[41]:


def IV_meas():
    gpib_inst = comm('5') 
    inst1 = gpib_inst.write('INST:SEL OUT1')
    inst1q = gpib_inst.query('INST:SEL?')
    volt1 = gpib_inst.query('MEAS:VOLT?')
    nvolt1 = scanf.scanf("%f", volt1)
    #for ele in nvolt1: 
    #    print(ele)
    curr1 = gpib_inst.query('MEAS:CURR?')
    ncurr1 = scanf.scanf("%f", curr1)
    #print('INST:SEL: ', inst1q, 'VOLT: ', nvolt1[0], 'CURR: ', ncurr1[0])

    inst2 = gpib_inst.write('INST:SEL OUT2')
    inst2q = gpib_inst.query('INST:SEL?')
    volt2 = gpib_inst.query('MEAS:VOLT?')
    nvolt2 = scanf.scanf("%f", volt2)
    curr2 = gpib_inst.query('MEAS:CURR?')
    ncurr2 = scanf.scanf("%f", curr2)
    #print('INST:SEL: ', inst2q, 'VOLT: ', nvolt2[0], 'CURR: ', ncurr2[0])

    return nvolt1, nvolt2, ncurr1, ncurr2

