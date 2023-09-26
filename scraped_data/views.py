from django.shortcuts import render,redirect
import os
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def scraper(request):
    return render(request, 'scraper.html')



def get_links(link,corelink) -> list:
    # filed = open("testfile.txt","a")
    visited = []
    visited.append(corelink)
    print("started get links")
    count = 0
    for i in link:
        try:
            print("\033[96m {}\033[00m" .format(i))
            if (i[0] == '/'):
                    # print("\033[93m {}\033[00m" .format(i))
                    i = corelink + i
                    print("\033[92m {}\033[00m" .format("completed link"))
                    print("\033[92m {}\033[00m" .format(i+"\n"))
            # print("\033[96m {}\033[00m" .format(i))
            if i == corelink:
                print("\033[97m {}\033[00m" .format("same link"))
                continue
            if i in visited:
                print("\033[97m {}\033[00m" .format("already visited"))
                continue
            response = requests.get(i)
            visited.append(i)
            print("\033[92m {}\033[00m" .format("got response from"+i+"\n"))
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all('a')
            links = [p.get('href') for p in links]
            # remove empty elements or none elements
            links = [p for p in links if p]
            # if element in all is a half link complete it with the link
            for p in range(len(links)):
                # complete half links with the main link
                if (links[p][0] == '/'):
                    print("\033[93m {}\033[00m" .format(links[p]))
                    links[p] = corelink + links[p]
                    print("\033[92m {}\033[00m" .format("completed link"))
                    # print("\033[92m {}\033[00m" .format(links[p]))
            # add the links to the main link
            link.extend(links)
            # remove duplicates
            link = list(set(link))
        except:
            print("\033[91m {}\033[00m" .format("error"))
            count += 1
            print("\033[91m {}\033[00m" .format(count))
    # for i in visited:
    #     filed.write(i+"\n")
    # filed.close()
    return visited


                # if (links[p][0] == '/'):
                #     print("\033[93m {}\033[00m" .format(links[p]))
                #     links[p] = corelink + links[p]
                #     print("\033[92m {}\033[00m" .format("completed link"))
                #     # print("\033[92m {}\033[00m" .format(links[p]))

def crawler(request):
    if request.method == 'POST':
        # get the link from the user
        link = request.POST.get('linked')
        if link=='':
            return render(request, 'crawler.html',{"message":"Please enter a link"})
        print(link)
        response = requests.get(link)
        print("got response")
        soup = BeautifulSoup(response.content, "html.parser")
        # get all the links from the soup
        links = soup.find_all('a')
        links = [i.get('href') for i in links]
        links.append(link)
        # remove empty elements or none elements
        links = [i for i in links if i]
        all = get_links(links,link)
        context = {
            'all': all,
        }
        return render(request, 'crawler.html',context)
    return render(request, 'crawler.html')

def output(request):
    if request.method == 'POST':
        print("request started output")
        # global context
        link = request.POST.get('linked','default')
        if link=='' or link == 'default':
            context = {
                "message":"Please enter a link"
            }
            return render(request, 'scraper.html',context)
        isembed = request.POST.get('output-type','default')
        getselector = request.POST.get('selector','default')
        print(getselector)
        if (isembed=='html' ):
            print("entered html")
            response = requests.get(link)
            print("got response")
            soup = BeautifulSoup(response.content, "html.parser")
            print("got soup")
            child_soup = soup.find_all(getselector)
            print(child_soup)
            attris = request.POST.get('attribute','default')
            all = []
            for i in child_soup:
                if(attris=='default'):
                    all.append(i.text)
                else:
                    all.append(i.get(attris))

            # remove empty elements or none elements
            all = [i for i in all if i]
            # if element in all is a half link complete it with the link
            for i in range(len(all)):
                if (all[i][0] == '/'):
                    all[i] = link + all[i]
            context = {
                'url': link,
                'selector': getselector,
                'attribute': attris,
                'all': all,
            }
            for i in child_soup:
                print(i.text)
            # print(context['htmlcontent'][0].text)
            return render(request, 'htmlform.html',context)
        elif (isembed == 'css'):
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            css = soup.find_all('link', rel='stylesheet')
            csslinks = []
            for i in css:
                csslinks.append(i.get('href'))
            for i in range(len(csslinks)):
                if (csslinks[i][0] == '/'):
                    csslinks[i] = link + csslinks[i]
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
            for i in range(len(jslinks)):
                if (jslinks[i][0] == '/'):
                    jslinks[i] = link + jslinks[i]
            context = {
                'csslinks':jslinks
            }
            return render(request, 'cssform.html',context)
    return render(request, 'error.html')