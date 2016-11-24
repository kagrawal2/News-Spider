from bs4 import BeautifulSoup
import requests
import re
import time
from datetime import datetime, timedelta
from automaticScraperConfig import *
import smtplib
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pickle
import operator



today = time.strftime("%m_%d_%Y")
print(today)

msg = '<!DOCTYPE html>'
msg += '<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /></head><body>'

additionalNews = 'Now fully automated, let me know if you find any problems' #Use this line to add custom News additions to send
msg += additionalNews

#cache reset for testing purposes
# cache = {}
# with open('/Users/kireet/Projects/NewsScraper/cache.pickle', 'wb') as handle:
#     pickle.dump(cache, handle)

#deleting two day old items
oldCache = pickle.load(open('/Users/kireet/Projects/NewsScraper/cache.pickle', 'rb'))
cache = {k:v for k,v in oldCache.items() if v != \
    (datetime.now() - timedelta(days = 3)).date()}

# def objectivityClassifier(titleString):
# http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
# http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_files.html#sklearn.datasets.load_files
#     http://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
#     http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_files.html
# http://machinelearningmastery.com/how-to-load-data-in-python-with-scikit-learn/


def techCrunch(url):
    try:
        global msg, cache
        # response = requests.get(url)
        # html = response.content
        f = urllib.request.urlopen(url)
        html = f.read()
        soup = BeautifulSoup(html)
        titles = soup.find_all(attrs={'class':'post-title'})
        # print(titles)
        # trending = soup.find_all(attrs={'class': 'trending-post'})
        # titleLinks = []
        tabooWords = ["how", 'we', 'you', "?", 'your', 'crunch', 'invite', 'invited']
        msg += ('<h2>Technology News</h2>')
        for title in titles:
            try:
                titleText = title.text.replace('\n', "").replace("\xa0", " ")
                # print(titleText.lower())
                # print(any(word not in titleText.lower() for word in tabooWords))
                if titleText not in cache.keys(): #check if in cache
                    cache[titleText] = datetime.now().date() #add to cache
                    if any(word not in titleText.lower() for word in tabooWords): # add Naive Bayes classification algorithm here
                        link = title.find('a', href=True)['href']
                        # titleLinks.append([titleText, link])
                        # spiderResponse = requests.get(link)
                        # spiderHtml = spiderResponse.content

                        spiderResponse = urllib.request.urlopen(link)
                        spiderHtml = spiderResponse.read()
                        spiderSoup = BeautifulSoup(spiderHtml)
                        paragraphs = spiderSoup.find(attrs={'class': 'article-entry text'})

                        sentences = []
                        try:
                            sentences = paragraphs.text.replace('\n', "").replace("\xa0", " ").split('.')
                        except:
                            print("Error at: " + paragraphs)

                        msg += ('<p><b>'  + titleText + '</b></p>')
                        msg += '<p>'

                        try:
                            i = 0
                            while i < 6 or len(sentences[i]) < 5:
                                msg += sentences[i] + '. '
                                i += 1
                        except:
                            print("Too few sentences")
                        msg += '</p>'
                        msg += '<a href="' + link + '">' + link + '</a>'
            except Exception as err:
                # print('Error here ' + str(err))
                continue
    except Exception as err:
        pass

techCrunch('https://techcrunch.com/startups/')


def marketReports():
    try:
        url = "http://www.marketwatch.com/markets/us"
        global msg, cache
        # response = requests.get(url)
        # html = response.content
        f = urllib.request.urlopen(url)
        html = f.read()
        soup = BeautifulSoup(html)
        articleList = soup.find(attrs={"class":"sixwide"})
        articleList = articleList.find_all(attrs={"class": "newsitem"})
        # print(articleList)
        tabooWords = ["how", 'we', '?', 'you']

        msg += '<h2>Market News</h2>'
        for article in articleList:
            try:
                articleText = [s for s in article.text.split('\n') if s][0].replace("\xa0", " ")
                if articleText not in cache.keys(): #check if in cache
                    cache[articleText] = datetime.now().date() #add to cache
                    if any(word not in articleText.lower() for word in tabooWords): # add Naive Bayes classification algorithm here
                        link = "http://www.marketwatch.com" + article.find('a', href=True)['href']
                        # print(link)
                        # spiderResponse = requests.get(link)
                        # print(spiderResponse)
                        # spiderHtml = spiderResponse.content
                        spiderResponse = urllib.request.urlopen(link)
                        spiderHtml = spiderResponse.read()
                        spiderSoup = BeautifulSoup(spiderHtml)
                        paragraphs = spiderSoup.find(attrs={'id': 'article-body'})
                        # print(paragraphs)
                        sentences = []
                        sentences = paragraphs.text.replace('\n', "").replace("\xa0", " ").split('.')
                        # print(sentences)
                        msg += '<p><b>'  + articleText + '</b></p>'
                        # print(articleText)
                        msg += '<p>'
                        i = 0
                        while i < 5 or len(sentences[i - 1]) < 5 or len(sentences[i]) < 5:
                            msg += sentences[i] + '. '
                            i += 1
                        msg += '</p>'
                        msg += '<a href="' + link + '">' + link + '</a>'

                        
            except Exception as err:
                # print('Error here' + err)
                continue
    except Exception as err:
        # print(err)
        pass
        
marketReports()

#saving cache
pickle.dump(cache, open('/Users/kireet/Projects/NewsScraper/cache.pickle', 'wb'))

msg += "</body></html>"

message = MIMEMultipart('alternative')
message['Subject'] = 'Report ' + today.replace('_', "-")
message['From'] = SENDER_EMAIL
message['To'] = RECEIVER_EMAIL

# # part2 = MIMEText('test', 'plain')
part2 = MIMEText(msg, 'html')

message.attach(part2)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(SENDER_EMAIL , SENDER_LOGIN) #defined in automaticScraperConfig.py
server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
server.quit()


