from bs4 import BeautifulSoup
import requests
import re
import time


today = time.strftime("%m_%d_%Y")
print(today)

ReportsFolder = "/Users/kireet/Projects/NewsScraper/Reports"
reportFile = ReportsFolder + "/" + today + '_Report.html'
with open(reportFile, 'w') as report:
    report.write('<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /></head><body>')
    report.close()


def techCrunch(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    titles = soup.find_all(attrs={'class':'post-title'})
    trending = soup.find_all(attrs={'class': 'trending-post'})
    # titleLinks = []
    tabooWords = ["how", 'we', 'you', "?", 'your']
    with open(reportFile, 'a') as report:
        report.write('<h2>Technology News</h2>')
        for title in titles:
            titleText = title.text.replace('\n', "").replace("\xa0", " ")
            # print(titleText.lower())
            # print(any(word not in titleText.lower() for word in tabooWords))
            if any(word not in titleText.lower() for word in tabooWords): # add Naive Bayes classification algorithm here
                link = title.find('a', href=True)['href']

                # titleLinks.append([titleText, link])
                spiderResponse = requests.get(link)
                spiderHtml = spiderResponse.content
                spiderSoup = BeautifulSoup(spiderHtml)
                paragraphs = spiderSoup.find(attrs={'class': 'article-entry text'})

                sentences = []
                try:
                    sentences = paragraphs.text.replace('\n', "").replace("\xa0", " ").split('.')
                except:
                    print("Error at: " + paragraphs)

                report.write('<p><b>'  + titleText + '</b></p>')
                report.write('<p>')
                i = 0
                while i < 6 or len(sentences[i]) < 5:
                    report.write(sentences[i] + '. ')
                    i += 1
                report.write('</p>')

        report.write("</body></html>")

techCrunch('https://techcrunch.com/startups/')


def marketReports():
    url = "http://www.marketwatch.com/markets"
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    articleList = soup.find(attrs={"class":"articlelist clear"})
    articleList = articleList.find_all('li')
    tabooWords = ["how", 'we', '?', 'you']

    with open(reportFile, 'a') as report:
        report.write('<h2>Market News</h2>')
        for article in articleList:
            try:
                articleText = article.text.split('\n\n')[3].replace("\xa0", " ")
                if any(word not in articleText.lower() for word in tabooWords): # add Naive Bayes classification algorithm here
                    link = article.find('a', href=True)['href']
                    spiderResponse = requests.get(link)
                    spiderHtml = spiderResponse.content
                    spiderSoup = BeautifulSoup(spiderHtml)
                    paragraphs = spiderSoup.find(attrs={'class': 'stri-full'})
                    sentences = []
                    try:
                        sentences = paragraphs.text.replace('\n', "").replace("\xa0", " ").split('.')
                        report.write('<p><b>'  + articleText + '</b></p>')
                        report.write('<p>')
                        i = 0
                        while i < 6 or len(sentences[i]) < 5:
                            report.write(sentences[i] + '. ')
                            i += 1
                        report.write('</p>')

                    except Exception as err:
                        print(err)

                        
            except:
                continue

        
marketReports()

with open(reportFile, 'a') as report:
    report.write("</body></html>")
    report.close()
                

