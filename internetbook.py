# -*- coding: cp949 -*-
from xmlbook import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import datetime, time

##global
conn = None
#regKey = '73ee2bc65b*******8b927fc6cd79a97'

# ���̹� OpenAPI ���� ���� information
server = "newsky2.kma.go.kr"

# smtp ����
host = "smtp.gmail.com" # Gmail SMTP ���� �ּ�.
port = "587"

def userURIBuilder(server,**user):
    str = "http://" + server + "/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?"
    for key in user.keys():
        str += key + '=' + user[key] + '&'
    print(str)
    return str

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)
        
def getBookDataFromISBN(local):






    global server, regKey, conn, dayMonth
    d = datetime.date.today()
    if d.month < 10:
        dayMonth = '0' + str(d.month)
    else:
        dayMonth = str(d.month)

    daystr = str(d.year) + dayMonth + str(d.day)
    regKey = "wVWM%2Fy12FdbMTHoWxdHSa%2BmdbN04QaafFDA6PF6bGaYyeSZ3t5KlwGhFm928pRHqcA%2FaPAD0g7v9TrPHmlKx1g%3D%3D"
    if conn == None :
        connectOpenAPIServer()
    uri = userURIBuilder(server, base_date=daystr, base_time="0200", nx="1", ny="1", serviceKey=regKey)
    conn.request("GET", uri)
    
    req = conn.getresponse()
    print (req.status)
    if int(req.status) == 200 :
        print("Book data downloading complete!")
        return extractBookData(req.read())
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None

def extractBookData(strXml):
    from xml.etree import ElementTree
    count = 0
    printWea = '0'
    tree = ElementTree.fromstring(strXml)
    print (strXml)
    # Book ������Ʈ�� �����ɴϴ�.
    itemElements = tree.getiterator("item")  # return list type
    print(itemElements)
    for item in itemElements:
        count += 1
        isbn = item.find("resultCode")
        dataTitle = item.find("fcstValue")
        if count == 1:
            print("���� Ȯ�� : ", dataTitle.text, "%")
        elif count == 2:
            if dataTitle.text == '0':
                printWea = "����"
            elif dataTitle.text == '1':
                printWea = "��"
            elif dataTitle.text == '2':
                printWea = "��/��"
            elif dataTitle.text == '3':
                printWea = "��"
            print("���� ���� : ", printWea)
            printWea = 0
        elif count == 3:
            print("6�ð� ������ : ", dataTitle.text, "mm")
        elif count == 4:
            print("���� : ", dataTitle.text, "%")
        elif count == 5:
            print("6�ð� ������ : ", dataTitle.text, "cm")
        elif count == 6:
            if dataTitle.text == '1':
                printWea = "����"
            elif dataTitle.text == '2':
                printWea = "���� ����"
            elif dataTitle.text == '3':
                printWea = "���� ����"
            elif dataTitle.text == '4':
                printWea = "�帲"
            print("�ϴ� ���� : ", printWea)
        elif count == 7:
            print("3�ð� ��� : ", dataTitle.text, "��")
        elif count == 8:
            print("��ħ ������� : ", dataTitle.text, "��")
        elif count == 9:
            print("ǳ�� : ", dataTitle.text, "m/s")
        elif count == 10:
            print("ǳ�� : ", dataTitle.text, "m/s")
            count = 0
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
    # MIMEMultipart�� MIME�� �����մϴ�.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #Message container�� �����մϴ�.
    msg = MIMEMultipart('alternative')

    #set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    
    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset = 'UTF-8')
    
    # �޼����� ������ MIME ������ ÷���մϴ�.
    msg.attach(msgPart)
    msg.attach(bookPart)
    
    print ("connect smtp server ... ")
    s = mysmtplib.MySMTP(host,port)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)    # �α��� �մϴ�. 
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
            html = MakeHtmlDoc(SearchBookTitle(value)) # keyword�� �ش��ϴ� å�� �˻��ؼ� HTML�� ��ȯ�մϴ�.
            ##��� �κ��� �ۼ�.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8')) #  ����( body ) �κ��� ��� �մϴ�.
        else:
            self.send_error(400,' bad requst : please check the your url') # �� ���� ��û��� ������ �����Ѵ�.
        
def startWebService():
    try:
        server = HTTPServer( ('localhost',8080), MyHandler)
        print("started http server....")
        server.serve_forever()
        
    except KeyboardInterrupt:
        print ("shutdown web server")
        server.socket.close()  # server �����մϴ�.

def checkConnection():
    global conn
    if conn == None:
        print("Error : connection is fail")
        return False
    return True
