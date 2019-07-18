from functools import reduce

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
#from selenium.webdriver.common.keys import Keys
#from selenium import webdriver
import re
import time
import os
import csv
import sys
import numpy
import operator
import gzip
import os
import shutil
import urllib.request
from os import listdir
from os.path import isfile, join
import subprocess
#from .models import Seed
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from Bio import SeqIO
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# changed part
import shutil
import urllib.request as req
from contextlib import closing

import requests
from bs4 import BeautifulSoup
from django.views.generic import TemplateView
import gzip
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.patches as mpatches
from os import listdir
from os.path import isfile, join
import numpy as np
import zipfile


from chartjs.views.lines import BaseLineChartView
import re
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline
from django.http import JsonResponse
from matplotlib.figure import Figure
import random
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib import pylab
from pylab import *
#import PIL, PIL.Image
#from io import StringIO
import matplotlib.lines as mlines
import matplotlib.ticker as ticker
import pdfkit

########PLOTLY########
import datetime
import glob
import logging
import os

import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.tools as tls
import plotly.plotly as py
import plotly.io as pio
# from ipywidgets import interactive, HBox, VBox, widgets, interact
######################

#cap = DesiredCapabilities().FIREFOX

xList = []
fileN = []
markList = []
posyList = []
eNumberList = []
posxEndList = []
# draw from summary
maxv = 0
maxtotal = 0
incount = 0
datalist = []
arr_rslt = []
faa_url = "https://www.ncbi.nlm.nih.gov"
direct_download_result = ""
faa_file_name = ""


diff=[]
seq_id=[]
rge=[]


key_list=[]
oupt_file=[]
lat_index=[]
value_2=[]
draw_graph_1_st=False
driver,URLentry, no_of_iteration,iter_entry,faa_path,dummy=(None,)*6

options = Options()
options.set_headless(headless=True)

def hmm_parse(opt,faa_path,gpreq):
    alldata_str_0 = []
    alldata_str_1 = []
    alldata1_str_1 = []
    alldata1_str_0 = []
    return_data=[]
    return_data1=[]
    all_data_xp=[]
    e_value_0=[]
    score_0=[]
    e_value_1 = []
    score_1 = []
    f = open(join(os.getcwd(),"media/hmm_output")).read()  # After building hmm_output, change the filename "test2.txt" to "hmm_output".
    data = f[f.find('    -'):f.find('\n\n\n')].split('\n')[3:]
    all_data = []
    all_data1=[]
    for line in data:
        if 'threshold' not in line:
            line = line.strip()
            all_data.append(list(map(float, re.split(r'\s+', line)[0:2])))
            all_data1.append(list(map(float, re.split(r'\s+', line)[3:5])))
            all_data_xp.append(list(map(str, re.split(r'\s+', line)[8:9])))
        else:
            break
    for line in all_data:
        alldata_str_0.append(str(line[0]))
        alldata_str_1.append(str(line[1]))
    for line in all_data1:
        alldata1_str_0.append(str(line[0]))
        alldata1_str_1.append(str(line[1]))
    for index,item in enumerate(alldata_str_0):
        if 'e-' in item:
            continue
        else:
            data_index=index
            break
    for index, item in enumerate(alldata1_str_0):
        if 'e-' in item:
            continue
        else:
            data1_index = index
            break
    all_data_xp=reduce(operator.concat,all_data_xp )
    #print (reduce(operator.concat,all_data_xp ))
    for index_g4 in range (0,data_index):
        return_data.append(all_data_xp[index_g4])
        e_value_0.append(alldata_str_0[index_g4])
        score_0.append(alldata_str_1[index_g4])
    for index_g4 in range (0,data1_index):
        return_data1.append(all_data_xp[index_g4])
        e_value_1.append(alldata1_str_0[index_g4])
        score_1.append(alldata1_str_1[index_g4])
    if gpreq==2:
        file_name = "./media/data/search_faa0.faa"
        f1 = (open(file_name, 'w'))
    else:
        file_name = "./media/data/graph3/search_faa0.faa"
        f1 = (open(file_name, 'w'))

    if opt==1:
        with open("./media/data/graph3/1_2.txt",'w') as one_f:
            one_f.writelines("E-Value  Score  Seq-Id")
            one_f.writelines("\n")
            for data_i,data_w in enumerate(e_value_0):
                one_f.writelines(data_w+"  "+score_0[data_i]+"  "+return_data[data_i])
                one_f.writelines("\n")

    #print (alldata_str_0[data_index]," ",alldata_str_1[data_index]," ",data_index-1)
    #print(alldata1_str_0[data1_index], " ", alldata1_str_1[data1_index]," ",data1_index-1)
        with open(faa_path) as f:
            datafile = f.readlines()
        #print (return_data)
        for index, line in enumerate(datafile):
            for item in return_data:
                #print (line)
                if item in (line):
                    f1.writelines(line)
                    stat = True
                    stat_index = index + 1
                    while (stat):
                        try:
                            if '>' in datafile[stat_index]:
                                stat = False
                                # f1.writelines(':::::::::::""""""""""::::::::::::::::::::::::::::::::"""""""""""""""""""""""""')
                                # f1.writelines('\n')
                            else:
                                f1.writelines(datafile[stat_index])
                            stat_index = stat_index + 1
                        except:
                            stat = False
                            break
    else:
        with open("./media/data/graph3/4_5.txt",'w') as one_f:
            one_f.writelines("E-Value  Score  Seq-Id")
            one_f.writelines("\n")
            for data_i,data_w in enumerate(e_value_1):
                one_f.writelines(data_w+"  "+score_1[data_i]+"  "+return_data1[data_i])
                one_f.writelines("\n")
        with open(faa_path) as f:
            datafile = f.readlines()
        print(return_data1)
        for index, line in enumerate(datafile):

            for item in return_data1:
                if item in line:
                    f1.writelines(line)
                    stat = True

                    stat_index = index + 1
                    #print(stat_index)
                    while (stat):
                        try:
                            if '>' in datafile[stat_index]:
                                stat = False
                                # f1.writelines(':::::::::::""""""""""::::::::::::::::::::::::::::::::"""""""""""""""""""""""""')
                                # f1.writelines('\n')
                            else:
                                f1.writelines(datafile[stat_index])
                            stat_index = stat_index + 1
                        except:
                            stat=False
                            #print ("exception")
                            break
        #print ("done")


def faafile_downloader(request):
    url = request.GET.get('url_name')
    print ("faa requeter")
    name = url.split("/")[-1]
    datapath_f = './media/'
    testfile = urllib.request.URLopener()
    testfile.retrieve(url, "new.gz")
    op_fn = os.path.splitext(name)[0]
    a = open("search.faa", 'w')
    with gzip.open("new.gz", 'rb') as f:
        for line in f:
            #print ("writing")
            a.writelines(line.decode('utf-8'))
    os.remove("new.gz")
    shutil.move("search.faa",join(datapath_f,"search.faa"))
    #file_path=join(join(join("http://localhost:8000","media"),"temp_download"),op_fn)
    #print (file_path)
    return JsonResponse({'file_name': "search.faa"})

def find_droop(path_all,faa_path_i,no_of_itera):

    faa_path = faa_path_i
    # print (fa)
    no_of_iteration = no_of_itera
    path = path_all


    value_0=[]
    lat_index = []
    value_2=[]

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
    #generate the text files

    value_2.pop(0)

    # print(key_list)
    for i in range(0, int(no_of_iteration)):
        file_name = "./media/data/search_faa" + str(i) + ".faa"
        f1 = (open(file_name, 'w'))
        key_list = []
        for ind in range(0, lat_index[i] - 1):
            key_list.append(value_2[ind])
        with open(faa_path) as f:
            datafile = f.readlines()
        for index, line in enumerate(datafile):
            for item in key_list:
                if item in line:
                    f1.writelines(line)
                    stat = True
                    stat_index = index + 1
                    while (stat):
                        try:
                            if '>' in datafile[stat_index]:
                                stat = False
                                # f1.writelines(':::::::::::""""""""""::::::::::::::::::::::::::::::::"""""""""""""""""""""""""')
                                # f1.writelines('\n')
                            else:
                                f1.writelines(datafile[stat_index])
                            stat_index = stat_index + 1
                        except:
                            stat = False
                            break
    #y_ret=run_thmm(no_of_iteration)
    #return y_ret

def find_droop_1(path_all,faa_path_i,no_of_itera):

    faa_path = faa_path_i
    # print (fa)
    no_of_iteration = no_of_itera
    path = path_all


    value_0=[]
    lat_index = []
    value_2=[]

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
    #generate the text files

    value_2.pop(0)

    # print(key_list)
    for i in range(0, int(no_of_iteration)):
        file_name = "./media/data/graph3/search_faa" + str(i) + ".faa"
        f1 = (open(file_name, 'w'))
        key_list = []
        for ind in range(0, lat_index[i] - 1):
            key_list.append(value_2[ind])
        with open(faa_path) as f:
            datafile = f.readlines()
        for index, line in enumerate(datafile):
            for item in key_list:
                if item in line:
                    f1.writelines(line)
                    stat = True
                    stat_index = index + 1
                    while (stat):
                        try:
                            if '>' in datafile[stat_index]:
                                stat = False
                                # f1.writelines(':::::::::::""""""""""::::::::::::::::::::::::::::::::"""""""""""""""""""""""""')
                                # f1.writelines('\n')
                            else:
                                f1.writelines(datafile[stat_index])
                            stat_index = stat_index + 1
                        except:
                            stat = False
                            break
    #y_ret=run_thmm(no_of_iteration)
    #return y_ret

def run_thmm(no_of_iteration):
    print (os.getcwd())
    datapath = './media/data'
    onlyfiles = [f for f in listdir(datapath) if isfile(join(datapath, f))]

    for fn in onlyfiles:
        if 'XP_' in fn:
            os.remove (os.path.join(datapath,fn))
    file_str="media/data/search_faa"+str(int(no_of_iteration)-1)+".faa"
    cmd="tmhmm -m "+os.path.join(os.getcwd(),"media/TMHMM2.0.model")+" -f " + os.path.join(os.getcwd(),file_str)
    hm = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True,cwd="./media/data").communicate()[0]
    x_ret=getPlotly2D_2('./media/data')
    return x_ret
    #print ("hm:", hm)

def next_prev_plot(p_path):
    x_ret = getPlotly2D_2(p_path)
    return x_ret

def run_thmm_zip(no_of_iteration):
    print (os.getcwd())
    datapath = './media/data'
    onlyfiles = [f for f in listdir(datapath) if isfile(join(datapath, f))]

    for fn in onlyfiles:
        if 'XP_' in fn:
            os.remove (os.path.join(datapath,fn))
    file_str="media/data/search_faa"+str(int(no_of_iteration))+".faa"
    cmd="tmhmm -m "+os.path.join(os.getcwd(),"media/TMHMM2.0.model")+" -f " + os.path.join(os.getcwd(),file_str)
    hm = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True,cwd="./media/data").communicate()[0]

def drawable(filename,plot_path):
    flag = False
    txt=plot_path+"/{}"
    with open(txt.format(filename), 'rb') as f:
        while True:
            line = f.readline()
            if line == '':
                continue
            if not line:
                break
            params = line.split()
            pos_start = int(params[0])
            pos_end = int(params[1])
            mark = str(params[2])
            if mark.find("in") != -1:
                if(pos_end - pos_start > 300):
                    flag = True
    return flag

def create_view(request):
    return render(request, 'home.html', {'file_name': False})

# I didn't change anything about this function
@csrf_exempt
def start_automation(request):
    if request.POST:
        # print(request.FILES['seed_input'].name)
        # print(request.POST.get('send_email_or_not'),request.POST.get('email'))

        # f = open(request.FILES['seed_input'].name,'w')
        # f.write(str(request.FILES['seed_input'].read().decode('ascii')))
        # f.close()
        toEmail = request.POST.get('email')
        flag = request.POST.get('flag');
        print(flag)
        '''
        if flag == "true":
            fn = request.FILES['seed_input']
            with open('./media/search.gz', "wb") as f:
                f.write(fn.read())
            f.close()
            with gzip.open('./media/search.gz', 'rb') as f_in:
                with open('./media/search.faa', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            f_out.close()
            f_in.close()

        else:
            #fn1 = request.FILES['seed_input1']
            with open('./media/search.faa', "w") as f:
                f.write(fn1.read().decode('ascii'))
            f.close()
        '''

        hm = subprocess.Popen("which hmmbuild", stdout=subprocess.PIPE, shell=True).communicate()[0]
        if 'hmmbuild' in str(hm):
            pass
        else:
            time.sleep(40)
            subprocess.Popen("sudo apt-get install hmmer", stdout=subprocess.PIPE, shell=True)

        # subprocess.Popen("hmmbuild media/profile.hmm "+str(request.FILES['seed_input'].name),shell=True)
        #subprocess.Popen("hmmbuild media/profile.hmm media/seed.txt", shell=True)
        #time.sleep(6)
        subprocess.Popen("hmmsearch media/profile.hmm media/search.faa > media/hmm_output", shell=True)
        time.sleep(5)
        if request.POST.get('send_email_or_not'):
            print('ajk')
            # your email id here
            fromaddr = "myemail@gmail.com"
            toaddr = request.POST.get('email')
            # instance of MIMEMultipart
            msg = MIMEMultipart()
            # storing the senders email address
            msg['From'] = fromaddr
            # storing the receivers email address
            msg['To'] = toaddr
            # storing the subject
            msg['Subject'] = "Output Hmm File"
            # string to store the body of the mail
            body = ""
            # attach the body with the msg instance
            msg.attach(MIMEText(body, 'plain'))
            # open the file to be sent
            filename = 'hmm_output'
            attachment = open("hmm_output", "rb")
            print(attachment)
            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')
            # To change the payload into encoded form
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(p)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()

            # add password here
            s.login(fromaddr, "7!*!")
            text = msg.as_string()
            s.sendmail(fromaddr, toaddr, text)
            s.quit()
        context = {'file_name': True}
        # return render(request, 'home.html',context)
        return JsonResponse({'code': 1})
    else:
        # return render(request, 'home.html',{'file_name':False})
        return JsonResponse({'code': 0})

    # Automation
    # driver = webdriver.Chrome(executable_path='/home/naveen/Downloads/chromedriver')
    # text_input = request.POST.get('input')
    # driver.get('https://pfam.xfam.org/')
    # driver.maximize_window()
    # time.sleep(5)
    # login = driver.find_element_by_id('jumpField')
    # login.send_keys(text_input)
    # driver.find_element_by_id('jumpButton').click()
    # time.sleep(3)
    # driver.find_element_by_id('alignBlockSelector').click()
    # time.sleep(3)
    # driver.find_element_by_tag_name('html').send_keys(Keys.CONTROL,Keys.END)
    # time.sleep(2)
    # driver.find_element_by_xpath("//select[@id='format']/option[@value='fasta']").click()
    # driver.find_element_by_xpath("//input[@type='submit' and @value='Generate']").click()
    # time.sleep(3)

    # print(request.FILES['seed_input'].read())
    # seed= Seed()
    # seed.seed_file = request.FILES['seed_input'].read()
    # seed.save()

# Download txt file.
@csrf_exempt
def searchTxtAndDownload(request):
    if request.POST:
        print(request.POST.get('user_id'))
        URL = "https://pfam.xfam.org/family/alignment/download/format"
        PARAMS = {
            'acc': request.POST.get('user_id'),
            'alnType': 'seed',
            'format': 'fasta',
            'order': 't',
            'case': 'l',
            'gaps': 'default',
            'download': '1'
        }
        # https://pfam.xfam.org/family/alignment/download/format?acc=PF00005&alnType=seed&format=fasta&order=t&case=l&gaps=default&download=1
        result = requests.get(url=URL, params=PARAMS)
        print(result.content)
        rltUrl = "https://pfam.xfam.org/family/alignment/download/format?acc=" + request.POST.get(
            'user_id') + "&alnType=seed&format=fasta&order=t&case=l&gaps=default&download=1"
        # with open("{0}_{1}.txt".format(request.POST.get('user_id'), PARAMS.get('alnType')), 'wb') as f:
        with open("./media/seed.txt", 'wb') as f:
            # Saving received content as a png file in
            # binary format

            # write the contents of the response (r.content)
            # to a new file in binary mode.
            f.write(result.content)
            print(f)
        f.close()
        # return render(request, 'home.html', {'file_name':False, "rltUrl":rltUrl, "downloaded":True})
        data = {'code': 1}
        return JsonResponse(data)
    return JsonResponse({'code': 0})

# Download faa file
def searchFaaAndDownload(request):
    global datalist
    global faa_url
    global arr_rslt
    global direct_download_result
    #print("i am in")
    print(request.GET.get('user_id'))
    URL = faa_url + '/genome'
    # Debaryomyces
    PARAMS = {
        "term": request.GET.get('user_id'),
        "EntrezSystem2.PEntrez.Genome2.Genome2_ResultsPanel.Genome2_DisplayBar.PageSize": 200
    }
    result = requests.get(url=URL, params=PARAMS)
    direct_download_result = result.content
    parsed_html = BeautifulSoup(result.content, "html.parser")
    arr_rslt = parsed_html.find_all('p', attrs={'class': 'title'})
    datalist = []
    hreflist = []
    for item in arr_rslt:
        URL = faa_url + item.find('a').get('href')
        print("url is:", URL)
        result = requests.get(url=URL)
        parsed_html = BeautifulSoup(result.content, "html.parser")
        tmp = parsed_html.find_all('span', attrs={'class': 'shifted'})
        linkurl = ""
        for tmp_item in tmp:
            tmp_list = tmp_item.find_all('a')

            for durl in tmp_list:
                if ('protein' in durl.text):
                    print("url_href:", durl.get('href'))
                    linkurl = durl.get('href')
        hreflist.append(linkurl)

    for item in arr_rslt:
        # print(item.find('a').text)
        # print(item.find('a').get('href'))
        datalist.append(item.find('a').text)
    print("datalist:", hreflist)

    return JsonResponse({"datalist": datalist, 'hreflist': hreflist})

def directFaaDownload(request):
    global faa_file_name
    parsed_html = BeautifulSoup(direct_download_result, "html.parser")
    tmp = parsed_html.find_all('span', attrs={'class': 'shifted'})
    for tmp_item in tmp:
        tmp_list = tmp_item.find_all('a')
        for durl in tmp_list:
            if (durl.text == 'protein'):
                print(durl.get('href'))
                str = durl.get('href').split('/')
                faa_file_name = str[-1]
                with closing(req.urlopen(durl.get('href'))) as r:
                    with open(faa_file_name, 'wb') as f:
                        shutil.copyfileobj(r, f)
                f.close()
                fn = faa_file_name
                fn = fn.replace('.gz', '')
                with gzip.open('search_faa.gz', 'rb') as f_in:
                    with open('./media/' + fn, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                f_out.close()
    return render(request, 'home.html', {'file_name': False, 'data_list': datalist})

@csrf_exempt
def faaDownload(request, id):
    item = arr_rslt[id]
    URL = faa_url + item.find('a').get('href')
    # Debaryomyces
    result = requests.get(url=URL)
    parsed_html = BeautifulSoup(result.content, "html.parser")
    tmp = parsed_html.find_all('span', attrs={'class': 'shifted'})
    faa_url_list = []
    for tmp_item in tmp:
        tmp_list = tmp_item.find_all('a')
        for durl in tmp_list:
            if (durl.text == 'protein'):
                print(durl.get('href'))
                str = durl.get('href').split('/')
                faa_file_name = str[-1]
                with closing(req.urlopen(durl.get('href'))) as r:
                    with open(faa_file_name, 'wb') as f:
                        shutil.copyfileobj(r, f)
                f.close()
                fn = faa_file_name
                fn = fn.replace('.gz', '')
                with gzip.open(faa_file_name, 'rb') as f_in:
                    with open('./media/' + 'search.faa', 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                f_out.close()
    return render(request, 'home.html', {'file_name': False, 'data_list': datalist})

# Draw Chart
def delete_column(self):
    # Instantiating a Workbook object by excel file path
    workbook = self.Workbook(self.dataDir + 'Book1.xls')

    # Accessing the first worksheet in the Excel file
    worksheet = workbook.getWorksheets().get(0)

    # Deleting a column from the worksheet at 2nd position
    worksheet.getCells().deleteColumns(1, 1, True)

    # Saving the modified Excel file in default (that is Excel 2003) format
    workbook.save(self.dataDir + "Delete Column.xls")

def getPlotimage(request):
    f = open('./media/hmm_output').read()  # After building hmm_output, change the filename "test2.txt" to "hmm_output".
    data = f[f.find('    -'):f.find('\n\n\n')].split('\n')[3:]
    all_data = []
    for line in data:
        if 'threshold' not in line:
            line = line.strip()
            all_data.append(list(map(float, re.split(r'\s+', line)[0:2])))
        else:
            break

    with open('./media/all_data.csv', 'wb') as f:
        np.savetxt(f, all_data, fmt='%.2e %.2f', delimiter=',')
    read_data = np.genfromtxt('./media/all_data.csv')
    x = list(x for x in range(read_data.shape[0]))
    y1 = [np.log10(x) for x in read_data[:, 0]]
    y2 = read_data[:, 1]

    xnew = np.linspace(min(x), max(x), 30)

    spl1 = make_interp_spline(x, y1, k=3)
    spl2 = make_interp_spline(x, y2, k=3)

    y1_new = spl1(xnew)
    y2_new = spl2(xnew)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    color = 'r'
    ax1.set_ylabel('score', color=color)
    ax1.plot(xnew, y2_new, color=color, linewidth=5)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.xaxis.set_ticks(np.arange(0, 460, 40))

    ax2 = ax1.twinx()

    color = 'k'
    ax2.set_ylabel('E-value', color=color)
    ax2.plot(xnew, y1_new, color=color, linewidth=5)
    ax2.tick_params(axis='y', labelcolor=color)

    y_labels = ax2.get_yticks()
    ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0e'))

    e_val = mlines.Line2D([], [], color='k',
                          marker='_', linestyle='None',
                          markersize=10, label='E-Value')

    score = mlines.Line2D([], [], color='r',
                          marker='_', linestyle='None',
                          markersize=10, label='Score')

    plt.legend(handles=[e_val, score])
    all_data1 = []

    f = open('./media/hmm_output').read()
    data1 = f[f.find('    -'):f.find('\n\n\n')].split('\n')[3:]

    for line in data1:
        if 'threshold' not in line:
            line = line.strip()
            all_data1.append(list(map(float, re.split(r'\s+', line)[0:1])))
            all_data1.append(list(map(float, re.split(r'\s+', line)[1:2])))
            all_data1.append(list(re.split(r'\s+', line)[8:9]))

        else:
            break

    np_array = np.reshape(np.array(all_data1), (-1, 3))
    pd.DataFrame(np_array).to_csv("./media/all_data1.csv")
    # print(np_array)

    df = pd.read_csv("./media/all_data1.csv")
    # If you know the name of the column skip this
    first_column = df.columns[0]
    # Delete first
    df = df.drop([first_column], axis=1)
    df.to_csv('./media/all_data1.csv', index=False)
    import io
    import base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.savefig('./media/plot.png')
    figdata_png = base64.b64encode(buf.getvalue())
    response = HttpResponse(figdata_png, content_type='image/png')
    return response

def result_artifact(iter):
    datapath = './media/'
    datapath_1='./media/data'

    artifacts_1_path=os.path.join(os.path.join(os.getcwd(),'media'),"Results")
    graph1 = join(artifacts_1_path,"Graph 1")
    graph2 = join(artifacts_1_path, "Graph 2")
    graph3=join(artifacts_1_path, "Graph 3")
    plot_1=join(datapath_1,"plot_1")
    plot_2=join(datapath_1,"plot_2")
    plot_3 = join(datapath_1, "plot_3")
    archive_path=join(datapath,'results.zip')
    if os.path.exists(archive_path):
        os.remove(archive_path)

    if os.path.exists(artifacts_1_path):
        shutil.rmtree(artifacts_1_path)
        os.mkdir(artifacts_1_path)
    else:
        os.mkdir(artifacts_1_path)
    if os.path.exists(graph1):
        shutil.rmtree(graph1)
        os.mkdir(graph1)
    else:
        os.mkdir(graph1)
    if os.path.exists(graph2):
        shutil.rmtree(graph2)
        os.mkdir(graph2)
    else:
        os.mkdir(graph2)
    if os.path.exists(graph3):
        shutil.rmtree(graph3)
        os.mkdir(graph3)
    else:
        os.mkdir(graph3)
    if os.path.exists(plot_1):

        shutil.rmtree(plot_1)
        os.mkdir(plot_1)
    else:
        os.mkdir(plot_1)
    if os.path.exists(plot_2):
        shutil.rmtree(plot_2)
        os.mkdir(plot_2)
    else:
        os.mkdir(plot_2)
    if os.path.exists(plot_3):
        a=0
        shutil.rmtree(plot_3)
        os.mkdir(plot_3)
    else:
        os.mkdir(plot_3)
    for item_file in os.listdir(datapath):
        if isfile (os.path.join(os.path.join(os.getcwd(),'media'),item_file)):
            if zipfile.is_zipfile(os.path.join(os.path.join(os.getcwd(),'media'),item_file)):
                b=0
            else:
                shutil.copy(os.path.join(os.path.join(os.getcwd(),'media'),item_file),os.path.join(graph1,item_file))

    for i_iter in range (0,int(iter)):
        print ("generating artifacts for plot ",str(i_iter+1))
        run_thmm_zip(i_iter)

        onlyfiles_1 = [f for f in listdir(datapath_1) if isfile(join(datapath_1, f))]

        str_pl="plot_"+str(int(i_iter)+1)
        path_pl=join(datapath_1,str_pl)
        for fn in onlyfiles_1:
            if 'XP_' in fn:
                shutil.copy(os.path.join(datapath_1, fn),join(path_pl,fn))
        file_name_faa= "search_faa"+str(int(i_iter))+".faa"
        shutil.copy(join(datapath_1,file_name_faa),join(path_pl,file_name_faa))
        plot_path_art=join(graph2,str_pl)
        os.mkdir(plot_path_art)
        for files in os.listdir(path_pl):
            shutil.copy(join(path_pl, files), join(plot_path_art, files))
        #shutil.copytree(path_pl, artifacts_1_path)
        #shutil.rmtree(path_pl)
        datapath_2 = './media/data'
        plot_no = "plot_" + str(i_iter+1)
        plot_pth = join(datapath_2, plot_no)
        getPlotly2D_2(plot_path_art,str(i_iter+1))
    if iter==0:
        html_path_gp3 = "./myapp/templates/temp-plot_graph3.html"
        pdf_file_name = "draw_graph_3.pdf"
        pdfkit.from_file(html_path_gp3, pdf_file_name)
        artifacts_1_path_pdf = graph3
        shutil.move(os.path.join(os.getcwd(), pdf_file_name), os.path.join(artifacts_1_path_pdf, pdf_file_name))
        for files_3 in os.listdir("./media/data/graph3"):
            shutil.copy(join("./media/data/graph3", files_3), join(graph3, files_3))

    print ("dg1 status ",draw_graph_1_st)
    if draw_graph_1_st==True:
        html_path_gp1 = "./myapp/templates/temp-plot.html"
        pdf_file_name = "draw_graph_1.pdf"
        pdfkit.from_file(html_path_gp1, pdf_file_name)
        artifacts_1_path_pdf = graph1
        shutil.move(os.path.join(os.getcwd(), pdf_file_name), os.path.join(artifacts_1_path_pdf, pdf_file_name))
    cmd="zip -r results.zip  "+ "Results"
    wd=join(os.getcwd(),"media")
    h=subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=wd,shell=True).communicate()[0]
    #shutil.make_archive("artifacts_1", 'zip', os.path.join(os.path.join(os.getcwd(), 'media'), "artifacts_1"))
    #shutil.rmtree(os.path.join(os.path.join(os.getcwd(), 'media'), "artifacts_1"))

def secondgraph(request):
    print ("second graph initilisation")
    option_g4=request.GET.get('opt')
    if option_g4=="None":
        return_val=find_droop("./media/all_data1.csv","./media/search.faa",request.GET.get('search'))
        #print (return_val)
        result_artifact(request.GET.get('search'))
    elif option_g4=="1-2":
        hmm_parse(1,"./media/search.faa",2)
        result_artifact(1)
    else:
        hmm_parse(2,"./media/search.faa",2)
        result_artifact(1)

    return JsonResponse({'plot': 1})

def get_plotv2_file(path_file):
    driver = webdriver.Firefox(executable_path=os.path.join(os.getcwd(), "geckodriver"), firefox_options=options)
    baseurl = "http://topcons.cbr.su.se/"
    stat_u=True
    print ("generating plotv2 file")
    while stat_u:
        try:
            driver.get(baseurl)
            driver.find_element_by_id("id_seqfile").send_keys(path_file)
            driver.find_element_by_name("do").click()
            status = driver.find_element_by_id('content_right_panel').text
            stat = True
            while (stat):
                if 'Finished' in status:
                    stat = False
                else:
                    try:
                        status = driver.find_element_by_id('content_right_panel').text
                    except:
                        continue
            element = driver.find_element_by_xpath('//a[contains(@href, "%s")]' % 'query.result.txt')
            print(element.get_attribute('href'))
            response = requests.get(element.get_attribute('href'))
            data = response.text
            f1 = open('./media/data/graph3/plotv2.txt', 'w')
            for line in data:
                f1.writelines(line)
                stat_u=False
        except Exception as e1:
            print (e1)
            continue

def thirdgraph(request):
    print ("third graph initilisation")
    print (request.GET.get('opt'))
    data_path=join("./media/data","graph3")
    if os.path.exists(data_path):

        shutil.rmtree(data_path)
        os.makedirs(data_path)
    else:
        os.makedirs(data_path)
    option_g4 = request.GET.get('opt')
    if option_g4 == "None":
        find_droop_1("./media/all_data1.csv", "./media/search.faa", 1)
    elif option_g4 == "1-2":
        hmm_parse(1, "./media/search.faa", 3)
    else:
        hmm_parse(2, "./media/search.faa", 3)
    path_file=join(os.getcwd(),'media/data/graph3/search_faa0.faa')
    get_plotv2_file(path_file)
    getPlotly2D_3(data_path)
    print ("plotting done")

    for files_data in os.listdir(data_path):
        #print ("files",files_data)
        if "_summary" in files_data:
            os.remove(join(data_path,files_data))

    result_artifact(0)

    return JsonResponse({'plot': 1})

def next_prev(request):
    '''
    datapath_2 = './media/data'
    plot_no="plot_"+str(request.GET.get('search'))
    plot_pth = join(datapath_2, plot_no)
    y_ret = next_prev_plot(plot_pth)
    #print (return_val)
    '''
    #return JsonResponse({'plot': y_ret})

def getPlotly2D(request):
    stat = True
    global draw_graph_1_st
    draw_graph_1_st=True
    while (stat):
        #print (stat)
        if (os.path.exists('./media/hmm_output')):
            stat = False
    time.sleep(5)
    f = open('./media/hmm_output').read()  # After building hmm_output, change the filename "test2.txt" to "hmm_output".
    data = f[f.find('    -'):f.find('\n\n\n')].split('\n')[3:]
    all_data = []
    for line in data:
        if 'threshold' not in line:
            line = line.strip()
            all_data.append(list(map(float, re.split(r'\s+', line)[0:2])))
        else:
            break

    with open('./media/all_data.csv', 'wb') as f:
        np.savetxt(f, all_data, fmt='%.2e %.2f', delimiter=',')
    read_data = np.genfromtxt('./media/all_data.csv')
    x = list(x for x in range(read_data.shape[0]))
    y1 = [np.log10(x) for x in read_data[:, 0]]
    y2 = read_data[:, 1]

    xnew = np.linspace(min(x), max(x), 30)

    spl1 = make_interp_spline(x, y1, k=3)
    spl2 = make_interp_spline(x, y2, k=3)

    y1_new = spl1(xnew)
    y2_new = spl2(xnew)

    fig, ax1 = plt.subplots()

    color = 'r'
    ax1.set_ylabel('score', color=color)
    ax1.plot(xnew, y2_new, color=color, linewidth=5)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.xaxis.set_ticks(np.arange(0, 460, 40))

    ax2 = ax1.twinx()

    color = 'k'
    ax2.set_ylabel('E-value', color=color)
    ax2.plot(xnew, y1_new, color=color, linewidth=5)
    ax2.tick_params(axis='y', labelcolor=color)

    y_labels = ax2.get_yticks()
    ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0e'))

    e_val = mlines.Line2D([], [], color='k',
                          marker='_', linestyle='None',
                          markersize=10, label='E-Value')

    score = mlines.Line2D([], [], color='r',
                          marker='_', linestyle='None',
                          markersize=10, label='Score')

    plt.legend(handles=[e_val, score])
    all_data1 = []

    f = open('./media/hmm_output').read()
    data1 = f[f.find('    -'):f.find('\n\n\n')].split('\n')[3:]

    for line in data1:
        if 'threshold' not in line:
            line = line.strip()
            all_data1.append(list(map(float, re.split(r'\s+', line)[0:1])))
            all_data1.append(list(map(float, re.split(r'\s+', line)[1:2])))
            all_data1.append(list(re.split(r'\s+', line)[8:9]))

        else:
            break

    np_array = np.reshape(np.array(all_data1), (-1, 3))
    pd.DataFrame(np_array).to_csv("./media/all_data1.csv")
    # print(np_array)

    df = pd.read_csv("./media/all_data1.csv")
    # If you know the name of the column skip this
    first_column = df.columns[0]
    # Delete first
    df = df.drop([first_column], axis=1)
    df.to_csv('./media/all_data1.csv', index=False)
    # plt.show()
    # fig = plt.gcf()
    # plotly_fig = tls.mpl_to_plotly(fig)
    # fig = go.Figure(data=data, layout=layout)
    trace1 = go.Scatter(
        x=xnew,
        y=y1_new,
        name='E-value',
        line={'color': 'rgba (0, 0, 0, 1)', 'dash': 'solid', 'width': 2.0}
    )
    trace2 = go.Scatter(
        x=xnew,
        y=y2_new,
        name='score',
        line={'color': 'rgba (255, 0, 0, 1)', 'dash': 'solid', 'width': 2.0},
        yaxis='y2'
    )
    data = [trace1, trace2]
    layout = go.Layout(
        title='',
        yaxis=dict(
            title='E-value',
            titlefont=dict(
                color='rgb(0,0,0)'
            ),
            tickfont=dict(
                color='rgb(0,0,0)'
            ),
            side='right',
            # exponentformat='e',
            tickformat="e",
        ),
        yaxis2=dict(
            title='score',
            titlefont=dict(
                color='rgb(255, 0, 0)'
            ),
            tickfont=dict(
                color='rgb(255, 0, 0)'
            ),
            overlaying='y',
            side='left',
            # exponentformat = 'e',
        ),

        legend=dict(
            x=0,
            y=1.16,
            traceorder='normal',
            font=dict(
                family='sans-serif',
                size=12,
                color='#000'
            ),
            bgcolor='#FFFFFF',
            bordercolor='#E2E2E2',
            borderwidth=2
        ),
    )

    plotly_fig = go.Figure(data=data, layout=layout)

    # plotly_fig['data'].append( dict(x=xnew, y=y2_new, type='scatter', mode='lines') )
    plot_div = plot(plotly_fig, output_type='file', include_plotlyjs=True, auto_open=False)
    shutil.move(plot_div, "./myapp/templates/temp-plot.html")
    return JsonResponse({'plot': plot_div})

def draw_with_summary(filename, plot_path, pos_y):
    global fileN, xList, markList, posyList,eNumberList, posxEndList,diff,seq_id,rge
    global maxv
    n = 0
    eNumber = 0
    diff = []
    seq_id = []
    rge = []
    #print ("draw summary")

    txt=plot_path+"/{}"
    first_entry=False
    with open(txt.format(filename), 'rb') as f:
        while True:
            line = f.readline()
            if line == '':
                continue
            if not line:
                break
            params = line.split()
            #print (filename)
            #print(params)
            pos_start = int(params[0])
            pos_end = int(params[1])
            mark = str(params[2])

            if mark.find("in") != -1:
                first_entry=True
                if (pos_end - pos_start > 300):
                    mk = 'i'
                    eNumber += 1
                else:
                    mk = 'o'
            elif mark.find("trans") != -1:
                first_entry=True
                mk = 't'
            else:
                if first_entry==True:
                    mk = 'o'
                elif (pos_end - pos_start > 300):
                    mk = 'o'
                else:
                    mk='dummy'
            #print(mark)
            markList.append(mk)
            posyList.append(pos_y)
            eNumberList.append(eNumber)
            n = n + 1
            xList.append([pos_start, pos_end])
            #print('ok', pos_start)
            if maxv <= pos_end:
                maxv = pos_end
    fileN.append(n)
    posxEndList.append(maxv)
    return n

def getPlotly2D_2(plot_path,iter):
    global fileN, xList, markList
    global maxv
    global maxtotal
    xList = []
    fileN = []
    markList = []
    # draw from summary
    maxv = 0
    maxtotal = 0
    incount = 0
    #print (os.getcwd())
    datapath=plot_path
    #datapath = './media/data'
    onlyfiles = [f for f in listdir(datapath) if isfile(join(datapath, f))]
    #print(onlyfiles)
    i = 0
    traceList = []
    yTickValue = []
    yTickName = []
    posxEndList = []
    pos_y = 50
    for fn in onlyfiles:
        if fn.find(".summary") != -1:
            if drawable(fn,plot_path) == False:
                continue
            maxv = 0
            incount = 0
            dataN = draw_with_summary(fn,datapath, pos_y=pos_y)
            yTickValue.append(pos_y)
            yTickName.append(fn.split(".")[0])
            pos_y += 50
            if maxtotal < maxv:
                maxtotal = maxv
            eStr = str(maxv) + "aa"
            trace = go.Scatter(x=[maxv+20], y=[pos_y-15], mode='text',showlegend=False, text=eStr, textfont=dict(color='rgb(0,0,0)'),
                               textposition='bottom right')
            traceList.append(trace)
            pos_y += 50
    #print(yTickValue, yTickName)
    layout = dict(title='',
                  yaxis=dict(
                      tickvals=yTickValue,
                      ticktext=yTickName,
                      showticklabels=True,
                  ),

                  )
    ind_1 = 0
    eStr = "Scale"
    trace = go.Scatter(x=[-70], y=[-40], mode='text', showlegend=False,text=eStr, textfont=dict(size=20, color='rgb(0,0,0)'))
    traceList.append(trace)
    maxv = 0
    ind_blue=0
    ind_red=0
    for ele in xList:
        pos_y = posyList[ind_1]
        mark = markList[ind_1]
        eNumber = eNumberList[ind_1]
        ind_1 = ind_1 + 1
        x1, x2 = ele[0], ele[1]
        if maxv < x2:
            maxv = x2
        if mark == 'i':
            # ellipse
            a = (x2 - x1) / 2
            b = 10.0
            xlist = []
            y1list = []
            y2list = []
            for xx in range(x2 - x1):
                x = xx - (x2 - x1) / 2
                y = b ** 2 - b ** 2 * x ** 2 / (a ** 2)
                if y <= 0:
                    y = 0
                else:
                    y = np.sqrt(y)
                xlist.append(x1 + xx)
                y1list.append(pos_y - y)
                y2list.append(pos_y + y)
            tracedown = go.Scatter(
                x=xlist,
                y=y1list,
                mode='lines',
                name='Inside',
                showlegend=False,
                line=dict(color='rgb(0, 0, 255)', width=4, shape='spline', smoothing=1.3)
            )
            traceup = go.Scatter(
                x=xlist,
                y=y2list,
                mode='lines',
                name='',
                showlegend=False,
                line=dict(color='rgb(0, 0, 255)', width=4, shape='spline', smoothing=1.3)
            )
            for y in range(-9, 10):
                x = a * a - a * a * y * y / (b * b)
                if x <= 0:
                    x = 0
                else:
                    x = np.sqrt(x)
                x0 = (x1 + x2) / 2
                if abs(y) < 3:
                    d = 3
                else:
                    d = 5
                xmin = x0 - x + d
                xmax = x0 + x - d
                if y == 0:
                    xmax += d
                if ind_blue==0:
                    trace = go.Scatter(x=[xmin, xmax], y=[y + pos_y, y + pos_y],name='Inside',mode = 'lines',showlegend=True,
                                   line=dict(dash='solid', color='rgb (0, 0, 255)', width=4))
                    traceList.append(trace)
                    ind_blue=1
                else:
                    trace = go.Scatter(x=[xmin, xmax], y=[y + pos_y, y + pos_y], mode='lines', showlegend=False,
                                       line=dict(dash='solid', color='rgb (0, 0, 255)', width=4))
                    traceList.append(trace)
            traceList.append(tracedown)
            traceList.append(traceup)
            eStr = "DBD" + str(eNumber)
            trace = go.Scatter(x=[int((x1 + x2) / 2)], y=[pos_y], mode='text', text=eStr,showlegend=False,
                               textfont=dict(color='rgb(255,255,255)'))
            traceList.append(trace)
            eStr1 = str(x1)
            eStr2 = str(x2)
            trace = go.Scatter(x=[x1], y=[pos_y + 40], mode='text', text=eStr1,showlegend=False, textfont=dict(color='rgb(0,0,0)'))
            traceList.append(trace)
            trace = go.Scatter(x=[x2], y=[pos_y + 40], mode='text', text=eStr2,showlegend=False, textfont=dict(color='rgb(0,0,0)'))
            traceList.append(trace)
        elif mark == 't':
            # Rectangle
            if  ind_red==0:
                trace = go.Scatter(x=[x1, x2], y=[pos_y, pos_y],name='Transmembrane helix',mode = 'lines',showlegend=True, line=dict(dash='solid', color='rgb (255, 0, 0)', width=20))
                traceList.append(trace)
                ind_red=1
            else:
                trace = go.Scatter(x=[x1, x2], y=[pos_y, pos_y], mode='lines',showlegend=False,
                                   line=dict(dash='solid', color='rgb (255, 0, 0)', width=20))
                traceList.append(trace)
        elif mark == 'o':
            # Line
            trace = go.Scatter(x=[x1, x2], y=[pos_y, pos_y], mode = 'lines',showlegend=False,line=dict(dash='solid', color='rgb (0, 0, 255)', width=1))
            traceList.append(trace)
    x2 = maxv - 200
    x1 = x2 - 50
    pos_y = posyList[-1]
    fig = dict(data=traceList, layout=layout)
    fig['layout'].update(margin=dict(l=100))
    #plotly_fig = go.Figure(data=data, layout=layout)
    #print(fig)
    # plotly_fig['data'].append( dict(x=xnew, y=y2_new, type='scatter', mode='lines') )
    plot_div = plot(fig, output_type='file', include_plotlyjs=True, auto_open=False)
    html_path="./myapp/templates/temp-plot_"+str(iter)+".html"
    shutil.move(plot_div, html_path)
    pdf_file_name="plot_"+str(iter)+".pdf"
    pdfkit.from_file(html_path,pdf_file_name)
    artifacts_1_path_pdf=os.path.join(os.path.join(os.getcwd(),'media'),"artifacts_1")
    shutil.move(os.path.join(os.getcwd(), pdf_file_name), os.path.join(plot_path, pdf_file_name))
    return plot_div

def Sort_Tuple(tup):
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if (tup[j][1] > tup[j + 1][1]):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup

def getPlotly2D_3(plot_path):
    global fileN, xList, markList
    global maxv
    global maxtotal
    xList = []
    fileN = []
    markList = []
    # draw from summary
    maxv = 0
    maxtotal = 0
    incount = 0
    # print (os.getcwd())
    datapath = plot_path
    # datapath = './media/data'
    file_name = []
    with open(join(plot_path,"plotv2.txt")) as ofile:
        line_o = ofile.readlines()
        file_no = 1
        sequence_name=[]
        for line_in, lines_1 in enumerate(line_o):
            count_i = 0
            i_line = ""
            m_line = ""
            o_line = ""
            if 'Sequence name' in lines_1:
                sequence_name.append(lines_1.split(":")[1].split(" ")[1])
            if 'TOPCONS predicted topology' in lines_1:
                line_data = line_o[line_in + 1]

                count_i = [(ind.start(), ind.end(), 'i') for ind in re.finditer('i+', line_data)]
                count_i = count_i + [(ind.start(), ind.end(), 'o') for ind in re.finditer('o+', line_data)]
                count_i = count_i + [(ind.start(), ind.end(), 'M') for ind in re.finditer('M+', line_data)]
                trace_data = Sort_Tuple(count_i)
                file_name.append(str(sequence_name[-1]) + "_summary.txt")

                f_opn = open(join("./media/data/graph3",file_name[-1]), 'w')

                if len(count_i) > 0:
                    for element in trace_data:
                        if element[2] == 'i':
                            i_line = str(element[0]) + " " + str(element[1]) + " inside"
                            f_opn.writelines(i_line)
                            f_opn.writelines("\n")
                        elif element[2] == 'o':
                            i_line = str(element[0]) + " " + str(element[1]) + " outside"
                            f_opn.writelines(i_line)
                            f_opn.writelines("\n")
                        else:
                            i_line = str(element[0]) + " " + str(element[1]) + " transmembrane helix"
                            f_opn.writelines(i_line)
                            f_opn.writelines("\n")

                file_no = file_no + 1


    onlyfiles = [f for f in listdir(datapath) if isfile(join(datapath, f))]
    print(onlyfiles)
    i = 0
    traceList = []
    yTickValue = []
    yTickName = []
    posxEndList = []
    pos_y = 50
    for fn in onlyfiles:
        if fn.find("_summary") != -1:
            if drawable(fn, plot_path) == False:
                continue
            maxv = 0
            incount = 0
            dataN = draw_with_summary(fn, datapath, pos_y=pos_y)
            yTickValue.append(pos_y)
            yTickName.append(fn.split(".")[0])
            pos_y += 50
            if maxtotal < maxv:
                maxtotal = maxv
            eStr = str(maxv) + "aa"
            trace = go.Scatter(x=[maxv + 20], y=[pos_y - 15], mode='text', showlegend=False, text=eStr,
                               textfont=dict(color='rgb(0,0,0)'),
                               textposition='bottom right')
            traceList.append(trace)
            pos_y += 50
    # print(yTickValue, yTickName)
    layout = dict(title='',
                  yaxis=dict(
                      tickvals=yTickValue,
                      ticktext=yTickName,
                      showticklabels=True,
                  ),

                  )
    ind_1 = 0
    eStr = "Scale"
    trace = go.Scatter(x=[-70], y=[-40], mode='text', showlegend=False, text=eStr,
                       textfont=dict(size=20, color='rgb(0,0,0)'))
    traceList.append(trace)
    maxv = 0
    ind_blue = 0
    ind_red = 0
    for ele in xList:
        pos_y = posyList[ind_1]
        mark = markList[ind_1]
        eNumber = eNumberList[ind_1]
        ind_1 = ind_1 + 1
        x1, x2 = ele[0], ele[1]
        if maxv < x2:
            maxv = x2
        if mark == 'i':
            # ellipse
            a = (x2 - x1) / 2
            b = 10.0
            xlist = []
            y1list = []
            y2list = []
            for xx in range(x2 - x1):
                x = xx - (x2 - x1) / 2
                y = b ** 2 - b ** 2 * x ** 2 / (a ** 2)
                if y <= 0:
                    y = 0
                else:
                    y = np.sqrt(y)
                xlist.append(x1 + xx)
                y1list.append(pos_y - y)
                y2list.append(pos_y + y)
            tracedown = go.Scatter(
                x=xlist,
                y=y1list,
                mode='lines',
                name='Inside',
                showlegend=False,
                line=dict(color='rgb(0, 0, 255)', width=4, shape='spline', smoothing=1.3)
            )
            traceup = go.Scatter(
                x=xlist,
                y=y2list,
                mode='lines',
                name='',
                showlegend=False,
                line=dict(color='rgb(0, 0, 255)', width=4, shape='spline', smoothing=1.3)
            )
            for y in range(-9, 10):
                x = a * a - a * a * y * y / (b * b)
                if x <= 0:
                    x = 0
                else:
                    x = np.sqrt(x)
                x0 = (x1 + x2) / 2
                if abs(y) < 3:
                    d = 3
                else:
                    d = 5
                xmin = x0 - x + d
                xmax = x0 + x - d
                if y == 0:
                    xmax += d
                if ind_blue == 0:
                    trace = go.Scatter(x=[xmin, xmax], y=[y + pos_y, y + pos_y], name='Inside', mode='lines',
                                       showlegend=True,
                                       line=dict(dash='solid', color='rgb (0, 0, 255)', width=4))
                    traceList.append(trace)
                    ind_blue = 1
                else:
                    trace = go.Scatter(x=[xmin, xmax], y=[y + pos_y, y + pos_y], mode='lines', showlegend=False,
                                       line=dict(dash='solid', color='rgb (0, 0, 255)', width=4))
                    traceList.append(trace)
            traceList.append(tracedown)
            traceList.append(traceup)
            eStr = "DBD" + str(eNumber)
            trace = go.Scatter(x=[int((x1 + x2) / 2)], y=[pos_y], mode='text', text=eStr, showlegend=False,
                               textfont=dict(color='rgb(255,255,255)'))
            traceList.append(trace)
            eStr1 = str(x1)
            eStr2 = str(x2)
            trace = go.Scatter(x=[x1], y=[pos_y + 40], mode='text', text=eStr1, showlegend=False,
                               textfont=dict(color='rgb(0,0,0)'))
            traceList.append(trace)
            trace = go.Scatter(x=[x2], y=[pos_y + 40], mode='text', text=eStr2, showlegend=False,
                               textfont=dict(color='rgb(0,0,0)'))
            traceList.append(trace)
        elif mark == 't':
            # Rectangle
            if ind_red == 0:
                trace = go.Scatter(x=[x1, x2], y=[pos_y, pos_y], name='Transmembrane helix', mode='lines',
                                   showlegend=True, line=dict(dash='solid', color='rgb (255, 0, 0)', width=20))
                traceList.append(trace)
                ind_red = 1
            else:
                trace = go.Scatter(x=[x1, x2], y=[pos_y, pos_y], mode='lines', showlegend=False,
                                   line=dict(dash='solid', color='rgb (255, 0, 0)', width=20))
                traceList.append(trace)
        elif mark == 'o':
            # Line
            trace = go.Scatter(x=[x1, x2], y=[pos_y, pos_y], mode='lines', showlegend=False,
                               line=dict(dash='solid', color='rgb (0, 0, 255)', width=1))
            traceList.append(trace)
    x2 = maxv - 200
    x1 = x2 - 50
    pos_y = posyList[-1]
    fig = dict(data=traceList, layout=layout)
    fig['layout'].update(margin=dict(l=100))
    # plotly_fig = go.Figure(data=data, layout=layout)
    # print(fig)
    # plotly_fig['data'].append( dict(x=xnew, y=y2_new, type='scatter', mode='lines') )
    plot_div = plot(fig, output_type='file', include_plotlyjs=True, auto_open=False)
    html_path = "./myapp/templates/temp-plot_graph3.html"
    shutil.move(plot_div, html_path)
    pdf_file_name = "graph3.pdf"
    pdfkit.from_file(html_path, pdf_file_name)
    #artifacts_1_path_pdf = os.path.join(os.path.join(os.getcwd(), 'media'), "artifacts_1")
    #shutil.move(os.path.join(os.getcwd(), pdf_file_name), os.path.join(plot_path, pdf_file_name))
    return plot_div

def draw_plot_graph_3(request):
    html_file="temp-plot_graph3.html"
    return render(request, html_file, {})

def draw_plot(request):
    html_file="temp-plot_"+str(request.GET.get('plot_no'))+".html"
    return render(request, html_file, {})

def draw_plot_graph_1(request):
    return render(request, "temp-plot.html", {})


class LineChartJSONView(BaseLineChartView):
    def __init__(self):
        self.f = open('./media/test2.txt').read()
        self.f = open('./media/test2.txt').read()
        self.data = self.f[self.f.find('    -'):self.f.find('\n\n\n')].split('\n')[3:]
        self.all_data = []
        for line in self.data:
            if 'threshold' not in line:
                line = line.strip()
                self.all_data.append(list(map(float, re.split(r'\s+', line)[0:2])))
            else:
                break
        with open('./media/all_data.csv', 'wb') as f:
            np.savetxt(f, self.all_data, fmt='%.2e %.2f', delimiter=',')
        self.read_data = np.genfromtxt('./media/all_data.csv')
        x = list(x for x in range(self.read_data.shape[0]))
        y1 = [np.log10(x) for x in self.read_data[:, 0]]
        y2 = self.read_data[:, 1]
        self.xnew = np.linspace(min(x), max(x), 30)

        spl1 = make_interp_spline(x, y1, k=3)
        spl2 = make_interp_spline(x, y2, k=3)

        self.y1_new = spl1(self.xnew)
        self.y2_new = spl2(self.xnew)

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return list(self.xnew)

    def get_providers(self):
        """Return names of datasets."""
        return ["score", "E-value"]

    def get_data(self):
        """Return 3 datasets to plot."""
        return [
            list(self.y1_new),
            list(self.y2_new)
        ]


line_chart_json = LineChartJSONView.as_view()

