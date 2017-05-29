# -*- coding: cp949 -*-
from xmlbook import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import datetime, time

##global
conn = None
#regKey = '73ee2bc65b*******8b927fc6cd79a97'

# 네이버 OpenAPI 접속 정보 information
server = "newsky2.kma.go.kr"

# smtp 정보
host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

class Local():

    def __init__(self, name, inX, inY):
        self.name = str(name)
        self.inX = str(inX)
        self.inY = str(inY)

def userURIBuilder(server,**user):
    str = "http://" + server + "/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?"
    for key in user.keys():
        str += key + '=' + user[key] + '&'
    #print(str)
    return str

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)
        
def getBookDataFromISBN(local):
    global server, regKey, conn, dayMonth, inX, inY, count
    localclass = []

    if local == '경기' or '경기도':
        inX = "60"
        inY = "120"
        localclass.append(Local('경기',60,120))
    if local == '서울' or '서울시' or '서울특별시':
        inX = "60"
        inY = "127"
        localclass.append(Local('서울', 60, 127))
    if local == '충북' or '충청북도':
        inX = "69"
        inY = "127"
        localclass.append(Local('충북', 69, 127))
    if local == '충남' or '충청남도':
        inX = "68"
        inY = "100"
        localclass.append(Local('충남', 68, 100))
    if local == '강원' or '강원도':
        inX = "73"
        inY = "134"
        localclass.append(Local('서울', 73, 134))
    if local == '경남' or '경상남도':
        inX = "91"
        inY = "77"
        localclass.append(Local('경남', 91, 77))
    if local == '경북' or '경상북도':
        inX = "89"
        inY = "91"
        localclass.append(Local('경북', 89, 91))
    if local == '전남' or '전라남도':
        inX = "51"
        inY = "67"
        localclass.append(Local('전남', 51, 67))
    if local == '전북' or '전라북도':
        inX = "63"
        inY = "89"
        localclass.append(Local('전북', 63, 89))
    if local == '인천' or '인천광역시':
        inX = "55"
        inY = "124"
        localclass.append(Local('인천', 55, 124))
    if local == '광주' or '광주광역시':
        inX = "58"
        inY = "74"
        localclass.append(Local('광주', 58, 74))
    if local == '대구' or '대구광역시':
        inX = "89"
        inY = "90"
        localclass.append(Local('대구', 89, 90))
    if local == '대전' or '대전광역시':
        inX = "67"
        inY = "100"
        localclass.append(Local('대전', 67, 100))
    if local == '울산' or '울산광역시':
        inX = "102"
        inY = "84"
        localclass.append(Local('울산', 102, 84))
    if local == '부산' or '부산광역시':
        inX = "98"
        inY = "76"
        localclass.append(Local('부산', 98, 76))
    if local == '제주' or '제주도':
        inX = "52"
        inY = "38"
        localclass.append(Local('제주', 52, 38))
    d = datetime.date.today()
    if d.month < 10:
        dayMonth = '0' + str(d.month)
    else:
        dayMonth = str(d.month)

    daystr = str(d.year) + dayMonth + str(d.day)
    regKey = "wVWM%2Fy12FdbMTHoWxdHSa%2BmdbN04QaafFDA6PF6bGaYyeSZ3t5KlwGhFm928pRHqcA%2FaPAD0g7v9TrPHmlKx1g%3D%3D"
    if conn == None :
        connectOpenAPIServer()
    if local == '전국':
        count = 0
        for count in localclass:
            uri = userURIBuilder(server, base_date=daystr, base_time="0200", nx=count.inX,
                                 ny=count.inY, serviceKey=regKey)
            conn.request("GET", uri)
            req = conn.getresponse()
            if int(req.status) == 200:
                #print("Book data downloading complete!")
                print(count.name)
                extractBookData(req.read())
            else:
                print("OpenAPI request has been failed!! please retry")
                return None
        return None

    uri = userURIBuilder(server, base_date=daystr, base_time="0200", nx=inX, ny=inY, serviceKey=regKey)
    conn.request("GET", uri)

    req = conn.getresponse()
    #print (req.status)


    if int(req.status) == 200 :
        #print("Book data downloading complete!")
        return extractBookData(req.read())
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None

def extractBookData(strXml):
    from xml.etree import ElementTree
    count = 0
    printWea = '0'
    tree = ElementTree.fromstring(strXml)
    # Book 엘리먼트를 가져옵니다.
    itemElements = tree.getiterator("item")  # return list type
    #print(itemElements)
    for item in itemElements:
        count += 1
        #isbn = item.find("resultCode")
        dataTitle = item.find("fcstValue")
        if count == 1:
            print("강수 확률 : ", dataTitle.text, "%")
        elif count == 2:
            if dataTitle.text == '0':
                printWea = "없음"
            elif dataTitle.text == '1':
                printWea = "비"
            elif dataTitle.text == '2':
                printWea = "비/눈"
            elif dataTitle.text == '3':
                printWea = "눈"
            print("강수 형태 : ", printWea)
            printWea = 0
        elif count == 3:
            print("6시간 강수량 : ", dataTitle.text, "mm")
        elif count == 4:
            print("습도 : ", dataTitle.text, "%")
        elif count == 5:
            print("6시간 신적설 : ", dataTitle.text, "cm")
        elif count == 6:
            if dataTitle.text == '1':
                printWea = "맑음"
            elif dataTitle.text == '2':
                printWea = "구름 조금"
            elif dataTitle.text == '3':
                printWea = "구름 많음"
            elif dataTitle.text == '4':
                printWea = "흐림"
            print("하늘 상태 : ", printWea)
        elif count == 7:
            print("3시간 기온 : ", dataTitle.text, "℃")
        elif count == 8:
            print("아침 최저기온 : ", dataTitle.text, "℃")
        elif count == 9:
            print("풍속 : ", dataTitle.text, "m/s")
        elif count == 10:
            print("풍향 : ", dataTitle.text, "m/s")
            count = 0
            print(" ")
        #if len(strTitle.text) > 0 :
        #   return {"category":isbn.text,"fcstValue":strTitle.text}


def sendMain():
    global host, port
    html = ""
    title = str(input ('Title :'))
    senderAddr = str(input ('sender email address :'))
    recipientAddr = str(input ('recipient email address :'))
    msgtext = str(input ('write message :'))
    passwd = str(input (' input your password of gmail account :'))
    msgtext = str(input ('Do you want to include book data (y/n):'))
    if msgtext == 'y' :
        keyword = str(input ('input keyword to search:'))
        html = MakeHtmlDoc(SearchBookTitle(keyword))
        html = MakeHtmlDoc(SearchBookTitle(keyword))

    import mysmtplib
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    #set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    
    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset = 'UTF-8')
    
    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(msgPart)
    msg.attach(bookPart)
    
    print ("connect smtp server ... ")
    s = mysmtplib.MySMTP(host,port)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)    # 로긴을 합니다. 
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()
    
    print ("Mail sending complete!!!")

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        from urllib.parse import urlparse
        import sys
      
        parts = urlparse(self.path)
        keyword, value = parts.query.split('=',1)

        if keyword == "title" :
            html = MakeHtmlDoc(SearchBookTitle(value)) # keyword에 해당하는 책을 검색해서 HTML로 전환합니다.
            ##헤더 부분을 작성.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8')) #  본분( body ) 부분을 출력 합니다.
        else:
            self.send_error(400,' bad requst : please check the your url') # 잘 못된 요청라는 에러를 응답한다.
        
def startWebService():
    try:
        server = HTTPServer( ('localhost',8080), MyHandler)
        print("started http server....")
        server.serve_forever()
        
    except KeyboardInterrupt:
        print ("shutdown web server")
        server.socket.close()  # server 종료합니다.

def checkConnection():
    global conn
    if conn == None:
        print("Error : connection is fail")
        return False
    return True
