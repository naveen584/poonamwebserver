from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import os
import subprocess 
from .models import Seed
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from Bio import SeqIO


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
import PIL, PIL.Image
from io import StringIO
import matplotlib.lines as mlines
import matplotlib.ticker as ticker

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
#from ipywidgets import interactive, HBox, VBox, widgets, interact
######################

cap = DesiredCapabilities().FIREFOX

datalist = []
arr_rslt = []
faa_url = "https://www.ncbi.nlm.nih.gov"
direct_download_result = ""
faa_file_name = ""

def create_view(request):

    return render(request, 'home.html',{'file_name':False})
# I didn't change anything about this function
@csrf_exempt
def start_automation(request):
    if request.POST:
        #print(request.FILES['seed_input'].name)
        #print(request.POST.get('send_email_or_not'),request.POST.get('email'))

        #f = open(request.FILES['seed_input'].name,'w')
        #f.write(str(request.FILES['seed_input'].read().decode('ascii')))
        #f.close()
        toEmail = request.POST.get('email')
        flag = request.POST.get('flag');
        print(flag)
        if flag == "true" :
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
            fn1 = request.FILES['seed_input1']
            with open('./media/search.faa', "w") as f:
                f.write(fn1.read().decode('ascii'))
            f.close()

        hm = subprocess.Popen("which hmmbuild",stdout=subprocess.PIPE ,shell=True).communicate()[0]
        if 'hmmbuild' in str(hm):
            pass
        else:
            time.sleep(40)
            subprocess.Popen("sudo apt-get install hmmer",stdout=subprocess.PIPE ,shell=True)

        #subprocess.Popen("hmmbuild media/profile.hmm "+str(request.FILES['seed_input'].name),shell=True)
        subprocess.Popen("hmmbuild media/profile.hmm media/seed.txt",shell=True)
        time.sleep(6)
        subprocess.Popen("hmmsearch media/profile.hmm media/search.faa > media/hmm_output",shell=True)
        time.sleep(5)
        if request.POST.get('send_email_or_not'):
            print('ajk')
            #your email id here
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

            #add password here
            s.login(fromaddr, "7!*!")
            text = msg.as_string()
            s.sendmail(fromaddr, toaddr, text)
            s.quit()
        context = {'file_name':True}
        #return render(request, 'home.html',context)
        return JsonResponse({'code':1})
    else:
        #return render(request, 'home.html',{'file_name':False})
        return JsonResponse({'code':0})

    #Automation
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

    #print(request.FILES['seed_input'].read())
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
            'acc':request.POST.get('user_id'),
            'alnType': 'seed',
            'format': 'fasta',
            'order': 't',
            'case': 'l',
            'gaps': 'default',
            'download': '1'
        }
        #https://pfam.xfam.org/family/alignment/download/format?acc=PF00005&alnType=seed&format=fasta&order=t&case=l&gaps=default&download=1
        result = requests.get(url=URL, params=PARAMS)
        print(result.content)
        rltUrl = "https://pfam.xfam.org/family/alignment/download/format?acc="+request.POST.get('user_id')+"&alnType=seed&format=fasta&order=t&case=l&gaps=default&download=1"
        #with open("{0}_{1}.txt".format(request.POST.get('user_id'), PARAMS.get('alnType')), 'wb') as f:
        with open("./media/seed.txt", 'wb') as f:
            # Saving received content as a png file in
            # binary format

            # write the contents of the response (r.content)
            # to a new file in binary mode.
            f.write(result.content)
            print(f)
        f.close()
        #return render(request, 'home.html', {'file_name':False, "rltUrl":rltUrl, "downloaded":True})
        data = {'code':1}
        return JsonResponse(data)
    return JsonResponse({'code':0})

# Download faa file
def searchFaaAndDownload(request):
    global datalist
    global faa_url
    global arr_rslt
    global direct_download_result
    print ("i am in")
    print(request.GET.get('user_id'))
    URL = faa_url+'/genome'
    #Debaryomyces
    PARAMS = {
         "term": request.GET.get('user_id'),
         "EntrezSystem2.PEntrez.Genome2.Genome2_ResultsPanel.Genome2_DisplayBar.PageSize": 200
    }
    result = requests.get(url=URL, params=PARAMS)
    direct_download_result = result.content
    parsed_html = BeautifulSoup(result.content, "html.parser")
    arr_rslt = parsed_html.find_all('p', attrs={'class':'title'})
    datalist = []
    hreflist = []
    for item in arr_rslt:
        URL = faa_url + item.find('a').get('href')
        # Debaryomyces
        result = requests.get(url=URL)
        parsed_html = BeautifulSoup(result.content, "html.parser")
        tmp = parsed_html.find_all('span', attrs={'class': 'shifted'})
        for tmp_item in tmp:
            tmp_list = tmp_item.find_all('a')
            linkurl = ""
            for durl in tmp_list:
                if (durl.text == 'protein'):
                    print(durl.get('href'))
                    linkurl = durl.get('href')
            hreflist.append(linkurl)

    for item in arr_rslt:
        #print(item.find('a').text)
        #print(item.find('a').get('href'))
        datalist.append(item.find('a').text)
    print("datalist:",datalist)

    return JsonResponse({"datalist":datalist, 'hreflist':hreflist})

def directFaaDownload(request):
    global faa_file_name
    parsed_html = BeautifulSoup(direct_download_result, "html.parser")
    tmp = parsed_html.find_all('span', attrs={'class': 'shifted'})
    for tmp_item in tmp:
        tmp_list = tmp_item.find_all('a')
        for durl in tmp_list:
            if(durl.text == 'protein'):
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
                    with open('./media/'+fn, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                f_out.close()
    return render(request, 'home.html', {'file_name':False, 'data_list':datalist})

@csrf_exempt
def faaDownload(request, id):
    item = arr_rslt[id]
    URL = faa_url+item.find('a').get('href')
    #Debaryomyces
    result = requests.get(url=URL)
    parsed_html = BeautifulSoup(result.content, "html.parser")
    tmp = parsed_html.find_all('span', attrs={'class': 'shifted'})
    faa_url_list = []
    for tmp_item in tmp:
        tmp_list = tmp_item.find_all('a')
        for durl in tmp_list:
            if(durl.text == 'protein'):
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
                    with open('./media/'+'search.faa', 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                f_out.close()
    return render(request, 'home.html', {'file_name':False, 'data_list':datalist})
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
    f = open('./media/hmm_output').read() #After building hmm_output, change the filename "test2.txt" to "hmm_output".
    data = f[f.find('    -'):f.find('\n\n\n')].split('\n')[3:]
    all_data = []
    for line in data:
        if 'threshold' not in line:
            line = line.strip()
            all_data.append(list(map(float, re.split(r'\s+', line)[0:2])))
        else:
            break

    with open('all_data.csv', 'wb') as f:
        np.savetxt(f, all_data, fmt='%.2e %.2f', delimiter=',')
    read_data = np.genfromtxt('all_data.csv')
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
    import io
    import base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.savefig('./media/plot.png')
    figdata_png = base64.b64encode(buf.getvalue())
    response = HttpResponse(figdata_png, content_type='image/png')
    return response


def getPlotly2D(request):
    f = open('./media/hmm_output').read()  # After building hmm_output, change the filename "test2.txt" to "hmm_output".
    data = f[f.find('    -'):f.find('\n\n\n')].split('\n')[3:]
    all_data = []
    for line in data:
        if 'threshold' not in line:
            line = line.strip()
            all_data.append(list(map(float, re.split(r'\s+', line)[0:2])))
        else:
            break

    with open('all_data.csv', 'wb') as f:
        np.savetxt(f, all_data, fmt='%.2e %.2f', delimiter=',')
    read_data = np.genfromtxt('all_data.csv')
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
    #plt.show()
    #fig = plt.gcf()
    #plotly_fig = tls.mpl_to_plotly(fig)
    #fig = go.Figure(data=data, layout=layout)
    trace1 = go.Scatter(
        x=xnew,
        y=y1_new,
        name='E-value',
        line = {'color': 'rgba (0, 0, 0, 1)', 'dash': 'solid', 'width': 2.0}
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
            titlefont = dict(
                color='rgb(0,0,0)'
            ),
                tickfont = dict(
                color='rgb(0,0,0)'
            ),
            side='right',
            #exponentformat='e',
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
            #exponentformat = 'e',
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


    #plotly_fig['data'].append( dict(x=xnew, y=y2_new, type='scatter', mode='lines') )
    plot_div = plot(plotly_fig, output_type='file', include_plotlyjs=True, auto_open=False)
    shutil.move(plot_div, "./myapp/templates/temp-plot.html")
    return JsonResponse({'plot':plot_div})

def draw_plot(request):
    return render(request, 'temp-plot.html', {})

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
