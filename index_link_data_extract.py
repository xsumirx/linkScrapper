from urllib.request import urlopen

import requests
from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup
import re
from multiprocessing import Queue
import urllib.parse
from idna import idnadata



class SearchedLink:
    def __init__(self):
        self.Name = ""
        self.Url = ""
        self.Des = ""

    def __repr__(self):
        return str(self.Name + " --- " + self.Url + "\n")


class AData:
    def __init__(self):
        self.link = ""
        self.name = ""

    def __repr__(self):
        return str(self.name + " --- " + self.link + "\n")


def checkVideoFile(fileName = ""):
    if fileName.endswith(('.mkv','.avi','.mp4')):
        return True
    else:
        return False

def parseLink(_strData):
    try:
        resData = re.search("(?P<url>https?://[^\s]+)", _strData).group("url")
        return resData
    except:
        return ""


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    CatchData = False
    CatchDataIndex = 0
    CatchDataList = []
    local_url_a_tag = ""

    def handle_starttag(self, tag, attrs):
        # global CatchData
        # global  CatchDataIndex
        # global CatchDataList
        if tag == "a":
            for name, value in attrs:
                if name == 'href' and checkVideoFile(value):
                    # print value
                    self.CatchData = True
                    tempAData = AData()
                    tempAData.link = self.local_url_a_tag +"/" + value
                    self.CatchDataList.append(tempAData)
                    self.CatchDataIndex = self.CatchDataList.index(tempAData)
                    break





    def handle_endtag(self, tag):
        return


    def handle_data(self, data):
        # global CatchData
        # global  CatchDataIndex
        # global CatchDataList
        if self.CatchData == True:
            self.CatchData = False
            self.CatchDataList[self.CatchDataIndex].name = data




def search_perform(_search_string, _search_extension):
    #----------Perform Google Search and Find the Result -----------------------


    DEBUG_VAR = True
    search_input = _search_string
    search_item = "intitle:index.of? "+_search_extension+" " + search_input
    base = "http://www.google.co.in"
    url_google_search = "http://www.google.co.in/search?q=" + search_item



    SearchResultCollection = []
    count=0
    query=search_item
    query=query.strip().split()
    query="+".join(query)

    html = "https://www.google.co.in/search?site=&source=hp&q="+query+"&gws_rd=ssl"
    req = urllib.request.Request(html, headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(urlopen(req).read(),"html.parser")


    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    # }
    #
    # response = requests.get(url_google_search,headers=headers)
    # soup = BeautifulSoup(response.text,"lxml")
    for item in soup.select(".r a"):
        if str(item.text).lower().startswith("index of /"):
            if DEBUG_VAR == True:
                print(item.text + "   |   " + parseLink(item.attrs['href']))
            tempSearchResultItem = SearchedLink()
            tempSearchResultItem.Name = item.text
            tempSearchResultItem.Url = parseLink(item.attrs['href'])
            SearchResultCollection.append(tempSearchResultItem)

    # for next_page in soup.select(".fl"):
    #     res = requests.get(base + next_page.get('href'))
    #     soup = BeautifulSoup(res.text,"lxml")
    #     for item in soup.select(".r a"):
    #         if str(item.text).lower().startswith("index of /"):
    #             print(item.text + "   |   " + parseLink(item.attrs['href']))
    #             tempSearchResultItem = SearchedLink()
    #             tempSearchResultItem.Name = item.text
    #             tempSearchResultItem.Url = parseLink(item.attrs['href'])
    #             SearchResultCollection.append(tempSearchResultItem)

    #------------Google Search Complete ------------------------------------------

    searchItemLen = len(SearchResultCollection)
    searchItemDone = 0;
    valuePrinted  = False
    parser = MyHTMLParser()
    returnString = ""
    if searchItemLen > 0:
        for sItem in SearchResultCollection:
            url_input = sItem.Url.split("/&sa")[0]
            try:
                url_input = urllib.parse.unquote(url_input)
            except Exception as ex:
                print("Error Parsing url....But Don't worry ! We are working on it" )

            if DEBUG_VAR == True:
                print("Sending Request.... for " + sItem.Name + "\n")
            print("Remaining.... " + str(searchItemLen-searchItemDone) + "\n")
            try:
                res = requests.get(url_input,timeout=5)
                parser.local_url_a_tag = url_input
                parser.feed(res.text)
            except Exception as ex:
                print("Timeout")
            searchItemDone += 1

        print("Total Links Collected - " + str(len(parser.CatchDataList)) + "\n")
        if len(parser.CatchDataList) > 0:
            #print([tempData.name for tempData in CatchDataList])
            #------------------Now Search What User Requested ------------------------
            for _localAdata in parser.CatchDataList:

                search_exploded = search_input.lower().split(" ")
                if all(_searchSub in str(_localAdata.name).lower() for _searchSub in search_exploded):
                    print(_localAdata.name + " -- " + _localAdata.link + "\n")
                    returnString += _localAdata.name + " -- " + _localAdata.link + "\n"
                    valuePrinted = True

            if valuePrinted == False:
                print("Sorry We couldn't find exact match - But you might wanna see what we found --")
                for _tempAData in parser.CatchDataList:
                    print(_tempAData.name + " - " + _tempAData.link )
                    returnString += _tempAData.name + " - " + _tempAData.link

            return returnString

    else:
        print("No Item Found !")
        returnString = "Nothing Found !"
        return returnString


searchValue = input("What to Search for >> ")
searchType = input("File Extenstion >> ")
search_perform(searchValue,searchType)