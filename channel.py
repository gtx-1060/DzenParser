import requests
import json
from bs4 import BeautifulSoup
from threading import Thread

class Channel:

    STATS_API_URL = "https://zen.yandex.ru/media-api/publication-view-stat?publicationId="
    ARTICLES_URL = "https://zen.yandex.ru/api/v3/launcher/more?channel_id="

    channelName = ""
    isNormalUrl = False
    oldLimit = -1
    statsResult = None

    def __init__(self, url : str):
        if (url.find("id/") != -1):
            self.authorId = url[url.find("id/")+3: len(url)]
        else:
            self.authorId = url[url.rfind("/")+1: len(url)]
            self.ARTICLES_URL = "https://zen.yandex.ru/api/v3/launcher/more?channel_name="
        #print(self.authorId)
        self.headers = { "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}
        try:
            page = requests.get(url,headers =self.headers)
            self.channelName = page.text[page.text.find("<title>")+7:page.text.find("|")-1]
            self.isNormalUrl = page.ok
        except Exception as e:
            print(e)
        
    def _getArticles(self, limit : int = 0):
        nextArticlesUrl = self.ARTICLES_URL+self.authorId
        result = {}
        for i in range(0,limit,20):
            try:
                resp = requests.get(nextArticlesUrl, headers =self.headers)
            except Exception as e:
                print(e)
            if (resp.ok):
                data = json.loads(resp.text)
                nextArticlesUrl = data["more"]["link"]
                for item in data["items"]:
                    result[item["link"]] = item["title"]
            else:
                break
            #print(nextArticlesUrl)
        return result

    def _getArticleStats(self, url : str, title : str):
        id = url[url.rfind("-")+1:url.rfind("?")]
        data = json.loads(requests.get(self.STATS_API_URL+id, headers=self.headers).text)
        data["title"] = title
        self.statsResult["names"].append(data["title"])
        self.statsResult["links"].append(url)
        self.statsResult["views"].append(data["views"])
        self.statsResult["readings"].append(data["viewsTillEnd"])
        self.statsResult["viewTime"].append(data["sumViewTimeSec"] / 60)
        self.statsResult["comments"].append(data["comments"])

    def getArticlesStats(self, limit : int = 10000):
        if (self.statsResult != None and limit == self.oldLimit):
            return self.statsResult
        if (not self.isNormalUrl):
            return {}
        self.oldLimit = limit
        articles = self._getArticles(limit)
        self.statsResult = {"title" : [], "names" : [], "views" : [], "readings" : [], "viewTime" : [], "comments" : [], "links" : []}
        for url in articles.keys():
            thread = Thread(target=self._getArticleStats, args = (url, articles[url]))
            thread.start()
            thread.join()
         
        return self.statsResult

#c = Channel("https://zen.yandex.ru/witchertop")
#c.getArticlesStats(20)