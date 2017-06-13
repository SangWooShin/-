# -*- coding:utf-8 -*-
loopFlag = 1
from xmlbook import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import datetime, time
import mysmtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox

#### Menu  implementation

def launcherFunction(menu):
    if menu == 'e':
        sendMail()
    elif menu == 'w':
        local = str(input ('도/광역시 를 입력하세요 :'))

    else:
        print ("error : unknow menu key")

##global
conn = None

# 메일에 보낼 정보
printStr = []
countDel = 0

# GUI
window = Tk()
window.geometry("420x450")
window.configure(background="pink")
photo = PhotoImage(file="koreanmap1.gif")
imageLabel = Label(window, image=photo)
imageLabel.pack()
imageLabel.place(x=20, y=100)

# global value
host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
port = "587"
htmlFileName = "logo.html"

senderAddr = "tlstkddn159@hamil.com.com"  # 보내는 사람 email 주소.
recipientAddr = "jay0927@kpu.ac.kr"  # 받는 사람 email 주소.

msg = MIMEBase("multipart", "alternative")
msg['Subject'] = "전국 도시 기상정보"
msg['From'] = senderAddr
msg['To'] = recipientAddr

# OpenAPI 접속 정보 information
server = "newsky2.kma.go.kr"
server2 = "openapi.airkorea.or.kr"

# smtp 정보
host = "smtp.gmail.com"  # Gmail SMTP 서버 주소.
port = "587"


class Local():
    def __init__(self, name, inX, inY, inPM10):
        self.name = str(name)
        self.inX = str(inX)
        self.inY = str(inY)
        self.inPM10 = str(inPM10)

    def printall(self):
        print(self.name, self.inPM10)


def userURIBuilder(server, **user):
    str = "http://" + server + "/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?"
    for key in user.keys():
        str += key + '=' + user[key] + '&'
    # print(str)
    return str


def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)


def getDataFromISBN(local):
    global server, regKey, conn, conn2, dayMonth, inX, inY, count, sendMailStr, printStr
    localclass = []
    sendMailStr = ' '

    printStr.clear()
    conn2 = HTTPConnection(server2)
    uri2 = "/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?itemCode=PM10&dataGubun=HOUR&pageNo=1&numOfRows=1&ServiceKey=wVWM%2Fy12FdbMTHoWxdHSa%2BmdbN04QaafFDA6PF6bGaYyeSZ3t5KlwGhFm928pRHqcA%2FaPAD0g7v9TrPHmlKx1g%3D%3D"
    conn2.request("GET", uri2)
    req2 = conn2.getresponse()

    if int(req2.status) == 200:
        tree2 = ElementTree.fromstring(req2.read())
        itemElements2 = tree2.getiterator("item")

    if local == "경기":
        inX = "60"
        inY = "120"
        for item in itemElements2:
            dataTitle = item.find("jeju")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('경기', 60, 120, dataTitle.text))

    if local == "서울":
        inX = "60"
        inY = "127"
        for item in itemElements2:
            dataTitle = item.find("seoul")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('서울', 60, 127, dataTitle.text))

    if local == "충북":
        inX = "69"
        inY = "127"
        for item in itemElements2:
            dataTitle = item.find("chungbuk")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('충북', 69, 127, dataTitle.text))

    if local == '충남':
        inX = "68"
        inY = "100"
        for item in itemElements2:
            dataTitle = item.find("chungnam")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('충남', 68, 100, dataTitle.text))

    if local == '강원':
        inX = "73"
        inY = "134"
        for item in itemElements2:
            dataTitle = item.find("gangwon")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('서울', 73, 134, dataTitle.text))

    if local == '경남':
        inX = "91"
        inY = "77"
        for item in itemElements2:
            dataTitle = item.find("gyeongnam")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('경남', 91, 77, dataTitle.text))

    if local == '경북':
        inX = "89"
        inY = "91"
        for item in itemElements2:
            dataTitle = item.find("gyeongbuk")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('경북', 89, 91, dataTitle.text))

    if local == '전남':
        inX = "51"
        inY = "67"
        for item in itemElements2:
            dataTitle = item.find("jeonnam")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('전남', 51, 67, dataTitle.text))

    if local == '전북':
        inX = "63"
        inY = "89"
        for item in itemElements2:
            dataTitle = item.find("jeonbuk")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('전북', 63, 89, dataTitle.text))

    if local == '인천':
        inX = "55"
        inY = "124"
        for item in itemElements2:
            dataTitle = item.find("incheon")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('인천', 55, 124, dataTitle.text))

    if local == '광주':
        inX = "58"
        inY = "74"
        for item in itemElements2:
            dataTitle = item.find("gwangju")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('광주', 58, 74, dataTitle.text))

    if local == '대구':
        inX = "89"
        inY = "90"
        for item in itemElements2:
            dataTitle = item.find("chungbuk")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('대구', 89, 90, dataTitle.text))

    if local == '대전':
        inX = "67"
        inY = "100"
        for item in itemElements2:
            dataTitle = item.find("daejeon")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('대전', 67, 100, dataTitle.text))

    if local == '울산':
        inX = "102"
        inY = "84"
        for item in itemElements2:
            dataTitle = item.find("ulsan")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('울산', 102, 84, dataTitle.text))

    if local == '부산':
        inX = "98"
        inY = "76"
        for item in itemElements2:
            dataTitle = item.find("busan")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('부산', 98, 76, dataTitle.text))

    if local == '제주':
        inX = "52"
        inY = "38"
        for item in itemElements2:
            dataTitle = item.find("jeju")
            print("미세먼지 농도(PM10) : ", dataTitle.text)
        localclass.append(Local('제주', 52, 38, dataTitle.text))

    d = datetime.date.today()
    if d.month < 10:
        dayMonth = '0' + str(d.month)
    else:
        dayMonth = str(d.month)

    sendMailStr = local + '<br>미세먼지 농도(PM10) :' + dataTitle.text
    printStr.append(str(local))
    printStr.append("\n")
    printStr.append('미세먼지 농도(PM10) : ')
    printStr.append(str(dataTitle.text))

    print(local)
    print("\n" + sendMailStr)

    daystr = str(d.year) + dayMonth + str(d.day)
    regKey = "wVWM%2Fy12FdbMTHoWxdHSa%2BmdbN04QaafFDA6PF6bGaYyeSZ3t5KlwGhFm928pRHqcA%2FaPAD0g7v9TrPHmlKx1g%3D%3D"
    if conn == None:
        connectOpenAPIServer()

    uri = userURIBuilder(server, base_date=daystr, base_time="0200", nx=inX, ny=inY, serviceKey=regKey)
    print(local, " , ", inX, " , ", inY)
    conn.request("GET", uri)

    req = conn.getresponse()
    if int(req.status) == 200:
        # print("Book data downloading complete!")
        return extractBookData(req.read())
    else:
        print("OpenAPI request has been failed!! please retry")
        return None


def extractBookData(strXml):
    from xml.etree import ElementTree
    global sendMailStr, printStr
    count = 0
    printWea = '0'
    tree = ElementTree.fromstring(strXml)
    # Book 엘리먼트를 가져옵니다.
    itemElements = tree.getiterator("item")  # return list type
    # print(itemElements)
    for item in itemElements:
        count += 1
        # isbn = item.find("resultCode")
        dataTitle = item.find("fcstValue")
        if count == 1:
            print("강수 확률 : ", dataTitle.text, "%")
            sendMailStr += '<br>강수 확률 : ' + dataTitle.text + "%"
            printStr.append('\n')
            printStr.append('강수 확률 : ')
            printStr.append(dataTitle.text)
            printStr.append('%')
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
            sendMailStr += "<br>강수 형태 : " + printWea
            printStr.append('\n')
            printStr.append('강수 형태률 : ')
            printStr.append(printWea)
            printWea = 0
        elif count == 3:
            print("6시간 강수량 : ", dataTitle.text, "mm")
            sendMailStr += "<br>6시간 강수량 : " + dataTitle.text + "mm"
            printStr.append('\n')
            printStr.append('6시간 강수량 : ')
            printStr.append(dataTitle.text)
            printStr.append('mm')
        elif count == 4:
            print("습도 : ", dataTitle.text, "%")
            sendMailStr += "<br>습도 : " + dataTitle.text + "%"
            printStr.append('\n')
            printStr.append('습도 : ')
            printStr.append(dataTitle.text)
            printStr.append('%')
        elif count == 5:
            print("6시간 신적설 : ", dataTitle.text, "cm")
            sendMailStr += "<br>6시간 신적설 : " + dataTitle.text + "cm"
            printStr.append('\n')
            printStr.append('6시간 신적설 : ')
            printStr.append(dataTitle.text)
            printStr.append('cm')
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
            sendMailStr += "<br>하늘 상태 : " + printWea
            printStr.append('\n')
            printStr.append('하늘 상태 : ')
            printStr.append(printWea)
        elif count == 7:
            print("3시간 기온 : ", dataTitle.text, "℃")
            sendMailStr += "<br>3시간 기온 : " + dataTitle.text
            printStr.append('\n')
            printStr.append('3시간 기온 : ')
            printStr.append(dataTitle.text)
        elif count == 8:
            print("아침 최저기온 : ", dataTitle.text, "℃")
            sendMailStr += "<br>아침 최저기온 : " + dataTitle.text
            printStr.append('\n')
            printStr.append('아침 최저기온 : ')
            printStr.append(dataTitle.text)
        elif count == 9:
            print("풍속 : ", dataTitle.text, "m/s")
            sendMailStr += "<br>풍속 : " + dataTitle.text
            printStr.append('\n')
            printStr.append('풍속 : ')
            printStr.append(dataTitle.text)
        elif count == 10:
            print("풍향 : ", dataTitle.text, "m/s")
            sendMailStr += "<br>풍향 : " + dataTitle.text
            printStr.append('\n')
            printStr.append('풍향 : ')
            printStr.append(dataTitle.text)
            printStr.append('m/s')
            count = 0

def askMail():
    global inputID
    RenderText.destroy()


    inputID = Entry(window, font='helvetica 12', width=20, borderwidth=12, relief='ridge')
    inputID.pack()
    inputID.place(x=50, y=150)
    okbutton = Button(window, text="확인", font='helvetica 12', command=sendMail)
    okbutton.pack()
    okbutton.place(x=115, y=200)






# 메일을 발송한다.
def sendMail():
    print(inputID.get())
    # MIME 문서를 생성합니다.
    htmlFD = open(htmlFileName, 'rb')
    HtmlPart = MIMEText(sendMailStr, 'html')
    htmlFD.close()

    # 만들었던 mime을 MIMEBase에 첨부 시킨다.
    msg.attach(HtmlPart)

    s = mysmtplib.MySMTP(host, port)
    # s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.



    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("tlstkddn159@gmail.com", "sangwoo159")
    s.sendmail(senderAddr, [inputID.get()], msg.as_string())
    s.close()
    print("Mail sending complete!!!")


def clicked():
    global countDel
    if countDel == 1:
        RenderText.destroy()
    InitRenderText()
    imageLabel.destroy()
    countDel = 1


def printMenu():
    TempFont = font.Font(window, size=20, weight='bold', family='Consolas')
    global MainText
    MainText = Label(window, font=TempFont, text="<전국 도시 기상정보 검색>")
    MainText.configure(background="pink")
    MainText.pack()
    MainText.place(x=20, y=40)

    global Label1
    Label1 = Label(window, font='helvetica 16', text="검색 목록")
    Label1.configure(background="pink")
    Label1.pack()
    Label1.place(x=290, y=150)

    global str1
    str1 = StringVar()

    global combo
    combo = ttk.Combobox(window, width=10, textvariable=str1)
    combo['value'] = ('경기', '서울', '인천', '강원', '충북', '충남', '경북', '경남', '전북', '전남', '광주',
                      '대구', '대전', '울산', '부산', '제주')
    combo.grid(column=0, row=0)
    combo.place(x=290, y=180)
    combo.current(0)

    global action
    action = Button(window, text="검색", font='helvetica 12', command=clicked)
    action.grid(column=0, row=1)
    action.place(x=290, y=220)

    # 여기 버튼부분 커맨드로 함수호출해주기
    button1 = Button(window, text="메일 보내기", font='helvetica 12', cursor="hand2", command=askMail)
    button1.pack()
    button1.place(x=290, y=300)



def InitRenderText():
    global RenderText

    RenderText = Text(window, width=35, height=23, borderwidth=12, relief='ridge')
    RenderText.pack()
    RenderText.place(x=10, y=100)
    RenderText.configure(state='normal')
    print(1)
    #RenderText.delete(0.0, END)
    getDataFromISBN((combo.get()))
    for i in printStr:
        RenderText.insert(INSERT, i)
    RenderText.insert(INSERT, "\n\n")


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        from urllib.parse import urlparse
        import sys

        parts = urlparse(self.path)
        keyword, value = parts.query.split('=', 1)

        if keyword == "title":
            html = MakeHtmlDoc(SearchBookTitle(value))  # keyword에 해당하는 책을 검색해서 HTML로 전환합니다.
            ##헤더 부분을 작성.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))  # 본분( body ) 부분을 출력 합니다.
        else:
            self.send_error(400, ' bad requst : please check the your url')  # 잘 못된 요청라는 에러를 응답한다.


def startWebService():
    try:
        server = HTTPServer(('localhost', 8080), MyHandler)
        print("started http server....")
        server.serve_forever()

    except KeyboardInterrupt:
        print("shutdown web server")
        server.socket.close()  # server 종료합니다.


def checkConnection():
    global conn
    if conn == None:
        print("Error : connection is fail")
        return False
    return True

##### run #####
while(loopFlag > 0):
    printMenu()
    window.mainloop()
else:
    print ("Thank you! Good Bye")