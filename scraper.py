from bs4 import BeautifulSoup
import requests
import re
import time


today = time.strftime("%d_%m_%Y")
print(today)

ReportsFolder = "/Users/kireet/Projects/NewsScraper/Reports"
reportFile = ReportsFolder + "/" + today + '_Report.txt'


def techCrunch(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    titles = soup.find_all(attrs={'class':'post-title'})
    trending = soup.find_all(attrs={'class': 'trending-post'})
    # titleLinks = []
    tabooWords = ["how", 'we', 'you', "?", 'your']
    with open(reportFile, 'w') as report:
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

                report.write(titleText + '\n')

                i = 0
                while i < 6 or len(sentences[i]) < 5:
                    report.write(sentences[i] + '.')


                    i += 1
                report.write('\n\n')



techCrunch('https://techcrunch.com/startups/')


            
        
    # for link in titleLinks[0:1]:
    #     spiderResponse = requests.get(link[1])
    #     spiderHtml = spiderResponse.content
    #     spiderSoup = BeautifulSoup(spiderHtml)
    #     paragraphs = spiderSoup.find(attrs={'class': 'article-entry text'})

    #     try:
    #         print(paragraphs.text.replace('\n', "").replace("\xa0", " ").split('.'))
    #     except:
    #         print("Error at: " + paragraphs)

    # print(titleLinks)


def marketReports():
    url = "http://www.marketwatch.com/markets"
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    articleList = soup.find(attrs={"class":"articlelist clear"})
    articleList = articleList.find_all('li')

    titleLinks = []
    tabooWords = ["how", 'we', '?', 'you']

    for article in articleList:
        if any(word not in article.text.lower() for word in tabooWords): # add Naive Bayes classification algorithm here
            try:
                titleLinks.append([article.text.split('\n\n')[3].replace("\xa0", " "), article.find('a', href=True)['href']])
            except:
                continue
    # print(titleLinks)

    for link in titleLinks[0:1]:
        spiderResponse = requests.get(link[1])
        spiderHtml = spiderResponse.content
        spiderSoup = BeautifulSoup(spiderHtml)
        paragraphs = spiderSoup.find(attrs={'class': 'stri-full'})
        
        try:
            print(paragraphs.text.replace('\n', "").replace("\xa0", " ").split('.'))
        except:
            print("Error at: " + paragraphs)

# marketReports()

# 




    # nestedTable = table.find('td')
    # rows = nestedTable.find_all('tr')

    # print(rows.find_all('td'))

    # headers = [header.text for header in rows.find_all('th')]
    # data = [td.get_text().strip() for td in rows.find_all('td')]
    # headers = [th.get_text().strip() for th in soup.find_all('th')]
    # print(headers)
    # tabledata = [td.get_text().strip() for td in soup.find_all(attrs={"class":"yfnc_tabledata1"})]


