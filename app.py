from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Tz9IL40q3kQ2Uj6z0ic3kyXBgWtQ9VDaE0mbBJk97nv5ot1ivG8dKrJzNwI/PDmZ20mv59V0tabcGZmYdjMYHV5BCQJ9ApxNN+6Zei9tj9d0cwQh7DwIkD6Y+nbIugzyzRMam8qKg1HLgMRaFpu07gdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('515763b2e36a823dac1f37fce98375ff')

# 找最大幣值
from bs4 import BeautifulSoup
import requests
import re

url = 'https://www.8591.com.tw/mallList-list.html?searchGame=859&searchServer=862&searchType=0&searchKey='
#Add User-Agent to the requests header
#https://stackoverflow.com/questions/41909065/scrape-data-with-beautifulsoup-results-in-404
headers = {"User-Agent":"Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
#print(soup.prettify())
def Mesos(n):
    try:
        return float(n)
    except ValueError:
        return float(0)


title_tag = soup.select("a.detail_link ")
NT2Mesos_List=[]
link_List=[]
Mesos_title_List=[]
count=0
max_mesos=0
for title in title_tag:
    link="https://www.8591.com.tw"+title["href"]
    link_List.append(link)
    Mesos_title=title.text
    Mesos_title_List.append(Mesos_title)
    str_num=title.text.find("1:")
    str_w=title.text.find("萬")
    #if(IsNum(title.text[str_num+2:str_w])==True):
    NT2Mesos_List.append(Mesos(title.text[str_num+2:str_w]))
for num in NT2Mesos_List:
    if(NT2Mesos_List[count]==max(NT2Mesos_List)):
        print(count)
        break
    count+=1
max_mesos=max(NT2Mesos_List)

print(link_List[count],Mesos_title_List[count])
print(NT2Mesos_List)
print('目前最大幣值為:',max(NT2Mesos_List))
NT2Mesos_List.remove(max(NT2Mesos_List))
print('目前第二大幣值為:',max(NT2Mesos_List))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 可透過修改程式裡的 handle_message() 方法內的程式碼來控制機器人的訊息回覆
@handler.add(MessageEvent, message=TextMessage)
def handle_message(link_List,Mesos_title_List,count):
    # message = TextSendMessage(text=event.message.text)
    # line_bot_api.reply_message(event.reply_token, message)
    # push message to one user
    # %0D%0A 換行
    message=TextSendMessage(text="目前最高幣值：1:"+str(max_mesos)+"\n"+link_List[count]+Mesos_title_List[count]) 
    line_bot_api.push_message('U77799c06e0cc27d4a6c27ad46ef43057',message)

handle_message(link_List,Mesos_title_List,count)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

