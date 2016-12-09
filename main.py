from httplib import HTTPSConnection,HTTPResponse,HTTPException,HTTPConnection
from HTMLParser import HTMLParser
import datetime


class ResultWriter:
    def __init__(self):
        self.dataFile = open("data.txt","a+")
        self.lineCounter = 0
        tempData = "************************************** " + str(datetime.datetime.now()) + " *******************************************" + '\n'
        self.dataFile.write(tempData)

    def put(self,data):
        self.lineCounter += 1
        self.dataFile.write(str(self.lineCounter)+ "  " + data + '\n')



class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)


record = Stack()
entry = ResultWriter()

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):

        if record.size() >= 1:
            if tag == "a":
                #Fetch the URL
                if len(attrs) > 0:
                    tpl = attrs[0]
                    if len(tpl) > 0:
                        for num in range(0,len(tpl)-1,2):
                            if tpl[num] == "href":
                                print tpl[num + 1]

        record.push(tag)
        return

    def handle_data(self, data):
        if record.size() >= 1:
            topVal = record.peek()
            if topVal == "body":
                print data
        return



    def handle_endtag(self, tag):
        if tag == "body":
            print "Body tag is being poped up"
        record.pop()
        return

    def handle_startendtag(self, tag, attrs):
        return




try:
    status_code = 0
    url = "dl3.upfilmvip.in"
    url_para = "/Movie/2016/"
    while status_code != 200:
        conn = HTTPConnection(url)
        conn.request("GET",url_para)
        resp1 = conn.getresponse()
        if resp1.status == 200:
            status_code = 200
        elif resp1.status == 302:
            status_code = 302
            url = resp1.getheader("Location")
            url = url.replace("https://","")
            url = url.replace("http://","")
            url_array = url.split('/',1)
            url = url_array[0];
            if len(url_array) > 1:
                url_para = '/' + url_array[1]
            else:
                url_para = ""
        else:
            status_code = 0
            break

    print resp1.status," ",resp1.msg
    data = resp1.read()
except HTTPException as ex:
    print ex.message

except Exception as e1:
    print e1.message


if status_code == 200:
    parser = MyHTMLParser()
    parser.feed(data)
    print "Success"
else:
    print "Failed"