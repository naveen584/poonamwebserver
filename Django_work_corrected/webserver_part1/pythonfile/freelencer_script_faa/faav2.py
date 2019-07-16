import csv
import sys
import os
import numpy
from tkinter import *
import tkinter as tk
from tkinter import filedialog
key_list=[]
oupt_file=[]
lat_index=[]
value_2=[]
driver,URLentry, no_of_iteration,iter_entry,faa_path,dummy=(None,)*6
def openfile():
    global URLentry
    folder_path = filedialog.askopenfilename()
    URLentry.delete(0, END)
    URLentry.insert(1, folder_path)

def openfile1():
    global URLentry
    folder_path = filedialog.askopenfilename()
    iter_entry.delete(0, END)
    iter_entry.insert(1, folder_path)


def find_droop():
    global URLentry,iter_entry,faa_path,path,lat_index,key_list,no_of_iteration,value_2
    value_0=[]

    with open(path) as csvfile:
        readCSV = csv.reader(csvfile)
        #print (readCSV)
        for row in readCSV:
            if row != []:
                value_0.append(row[0])
                value_2.append(row[2])
    list_0=[]
    for vaues in value_0:
        list_0.append(float(vaues))
    list_0.pop(0)
    #print(list_0)


    diff_list= ([abs(100.0 * (a2-a1/a2) )for a1, a2 in zip(list_0[1:], list_0)])
    print (diff_list)
    #print (max(diff_list))
    '''
    a = numpy.array(list_0, dtype=float)
    for item in numpy.diff(a)/ a[:,1:] * 100:
        diff_list.append(float(item))
    print (diff_list)
    #print (len(diff_list))
    #print (max(diff_list))
    '''
    maxima=[]
    diff_lis_copy_dmmy=[]
    for item in diff_list:
        diff_lis_copy_dmmy.append(item)
    for ind in range (0,int(no_of_iteration)):
        maxima.append(float(max(diff_lis_copy_dmmy)))
        diff_lis_copy_dmmy.remove(maxima[-1])
    print (maxima)
    #print (diff_list)

    for ind,item in enumerate(maxima):
        #print (maxima[ind])
        for i,j in enumerate(diff_list):
            #print (j)
            if j==maxima[ind]:
                #print ("index ",i)
                lat_index.append(i+2)
    print (lat_index)


    copy_value()

def copy_value():
    global key_list,faa_path,no_of_iteration,oupt_file
    value_2.pop(0)

    #print(key_list)
    for i in range(0,int(no_of_iteration)):
        file_name="search_faa"+str(i)+".faa"
        f1=(open(file_name,'w'))
        key_list=[]
        for ind in range(0, lat_index[i] - 1):
            key_list.append(value_2[ind])
        with open(faa_path) as f:
            datafile = f.readlines()
        for index,line in enumerate (datafile):
            for item in key_list:
                if item in line:
                    f1.writelines(line)
                    stat=True
                    stat_index=index+1
                    while(stat):
                        if '>' in datafile[stat_index]:
                            stat=False
                            #f1.writelines(':::::::::::""""""""""::::::::::::::::::::::::::::::::"""""""""""""""""""""""""')
                            #f1.writelines('\n')
                        else:
                            f1.writelines(datafile[stat_index])
                        stat_index=stat_index+1



def scrap():
    global no_of_iteration,root1,path,faa_path
    print (sys.argv)
    faa_path=sys.argv[2]
    #print (fa)
    no_of_iteration=sys.argv[3]
    path=sys.argv[1]

    find_droop()




scrap()

