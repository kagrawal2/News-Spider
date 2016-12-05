from bs4 import BeautifulSoup
import requests

class URLNode(object):
    """Stores a URL for later scraping"""
    def __init__(self, url = None, parent = None):
        self.url = url
        self.parentNode = parent
        self.children = []

    def getUrl(self):
        return self.url

    def addChildren(self, children):
        #Allows for multiple children to be added
        self.children.append(children)

    def getChildren(self):
        return self.children 

class Scraper(object):
    """General Scraper Object which returns the attribute and future level
    Input takes inital url and a list of tuple pairs for recursive scraping.
    Outputs a Tree of URLs where the level of the URL node is the distance from the inital url
    Usage: Scraper(initURL, [['class', 'first-level'], ['id', 'second-level'], ['class', 'third-level']])
    """
    def __init__(self, url, *args):
        self.args = []
        for arg in args:
            self.args.append(arg)

        self.root = URLNode(url = url)
        self.height = len(*args)


    def singleScrape(url, attr, identity): #private
        try:
            response = requests.get(url)
            html = response.content
            soup = BeautifulSoup(html)
            findAttr = soup.find_all(attrs= {str(attr) : str(identity)})
            """Do something with findAttr if desired"""

            links = []
            for item in findAttr:
                link = item.find('a', href=True)['href']
                links.append(link)
            return links
        except:
            return 1

    def populateScrape(self, currNode, currentLevel): #private
        if currentLevel >= self.height:
            return self.root
        else:
            links = singleScrape(currNode.getUrl(), self.args[currentLevel])
            currentLevel += 1
            currNode.addChildren(links)
            for child in currNode.getChildren():
                self.populateScrape(child, currentLevel)

    def scrape(self): #public
        return self.populateScrape(self.root, 0)


