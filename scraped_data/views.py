from django.shortcuts import render,redirect
import os
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def output(request):
    global context
    link = request.POST.get('linked','default')
    isembed = request.POST.get('output-type','default')
    if (isembed=='html' ):
        response = requests.get(link)
        context = {
            'htmlcontent':response.text
        }
        return render(request, 'htmlform.html',context)
    elif (isembed == 'css'):
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        css = soup.find_all('link', rel='stylesheet')
        csslinks = []
        for i in css:
            csslinks.append(i.get('href'))
        context = {
            'csslinks':csslinks
        }
        return render(request, 'cssform.html',context)
    elif (isembed == 'js'):
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        js = soup.find_all('script')
        jslinks = []
        for i in js:
            if(i.get('src')!=None):
                jslinks.append(i.get('src'))
        context = {
            'csslinks':jslinks
        }
        return render(request, 'cssform.html',context)
    return render(request, 'error.html')