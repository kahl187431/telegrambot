import time
import telepot
import os
from bs4 import BeautifulSoup
import urllib.request as req
import re


botToken = "1441482635:AAG75IZjfWnLFkJOUWh6jK9JT6wj8zZjjjs"
bot = telepot.Bot(botToken)

InfoMsg = "안녕하세요. 지니입니다.\n" \
          "요청할 메뉴를 선택하세요.\n" \
          "1. 환율.\n" \
          "2. 주가.\n" \
          "3. 날씨.\n" \
          "4. 종료.\n"

status = True



def handle(msg):
    content, chat, id = telepot.glance(msg)
    print(content, chat, id)

    if content == 'text':
 #환율 확인==========================================================================
        if msg['text'] == '1' or msg['text'] == '환율':
            bot.sendMessage(id, '환율를 확인합니다.')
            #네이버환율에서 크롤링
            url = "https://finance.naver.com/marketindex/"

            res = req.urlopen(url)
            soup = BeautifulSoup(res,"html.parser", from_encoding = "euc-kr")

            name_nation = soup.select("h3.h_lst > span.blind")
            name_price = soup.select("span.value")
            name_change = soup.select("span.change")
            
            i = 0
            for c_list in soup:
                try:
                    print(i+1,name_nation[i].text, name_price[i].text)
                    if " " in name_change[i].text:
                        change = name_change[i].text + " 하락"
                    else: 
                        change = name_change[i].text + " 상승"
                    bot.sendMessage(id, str(i+1) + "  " + name_nation[i].text +" : "+ name_price[i].text + " , " + change)
                    i = i+1
                except IndexError:
                    pass
            
            bot.sendMessage(id, '환율정보 업데이트 완료.')

#네이버 주식에서 시가총액 상위 top10 지수 확인==================================================================
        elif msg['text'] == '2' or msg['text'] == '주가':
            bot.sendMessage(id, '주가를 확인합니다.')
            
            url = "https://finance.naver.com/sise/sise_market_sum.nhn"

            res = req.urlopen(url)
            soup = BeautifulSoup(res,"html.parser", from_encoding = "euc-kr")

            data = []
            table = soup.find('table', {'class' : 'type_2'})
            table_body = table.find('tbody')
            rows = table_body.findAll('tr',{'onmouseover' : 'mouseOver(this)'})
            
            i = 0
            for row in rows:
                
                cols = row.findAll('td')
                
                if len(cols) > 5:
                    title = cols[1].find(text=True)
                    price = cols[2].find(text=True)
                    dif_price = cols[3].find('span').text
                    dif_price = dif_price.strip()
                    dif_per = cols[4].find('span').text
                    dif_per = dif_per.strip()
                    foreign = cols[8].find(text=True)
                    totalPrice = cols[6].find(text=True)
                    per = cols[10].find(text=True)
                    roe = cols[11].find(text=True)
                
                bot.sendMessage(id, str(i+1) +" | 종목명 : "+ title +" | 현재가 : "+ price + " | 전일비 : " + dif_price + " | 등락률 : " + dif_per + " | 외국인비율 : " + foreign + " | 시가총액 : " + totalPrice + " | PER : " + per + " | ROE : " + roe )
                if i+1 == 10: 
                    bot.sendMessage(id, '주가정보 업데이트 완료.')
                    break
                i = i+1


   #네이버 날씨에서 오늘 날씨 확인===============================================================================
        elif msg['text'] == '3' or msg['text'] == '날씨':
            bot.sendMessage(id, '검색할 지역을 알려주세요.')
            location = input(msg['text'])

            url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="+location+"+날씨"

            res = req.urlopen(url)
            soup = BeautifulSoup(res,"html.parser", from_encoding = "euc-kr")

            todaytemp = str(soup.select("span.todaytemp"))
            todaytemp = re.sub('<.+?>', '', todaytemp, 0).strip()
            tempmark = str(soup.select("span.tempmark"))
            tempmark = re.sub('<.+?>', '', tempmark, 0).strip()
            mintemp = str(soup.select("span.min"))
            mintemp = re.sub('<.+?>', '', mintemp, 0).strip()
            maxtemp = str(soup.select("span.max"))
            maxtemp = re.sub('<.+?>', '', maxtemp, 0).strip()
            sensible = str(soup.select("span.sensible"))
            sensible = re.sub('<.+?>', '', sensible, 0).strip()

            print(todaytemp)
            print(tempmark)
            print(mintemp)
            print(maxtemp)
            print(sensible)

         


        elif msg['text'] == '4' or msg['text'] == '종료' or msg['text'] == 'out':
            bot.sendMessage(id, '챗봇을 종료합니다.')
            

        elif '지니' in msg['text'] or 'hi' in msg['text'] or 'hello' in msg['text']:
            bot.sendMessage(id, InfoMsg)    
        else:
            bot.sendMessage(id, 'Incorrect Command')
            bot.sendMessage(id, InfoMsg)  


bot.message_loop(handle)

while status == True:
    time.sleep(10)