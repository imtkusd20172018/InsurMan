from flask import Flask, send_file, send_from_directory, request, jsonify, render_template, abort
from getData.weather import getWeather
from getData.runAIML import runAIML
from getData.stock2 import getfixstock
from getData.oilPrice import getOilPrice
from getData.golden import getGolden
from getData.Currency import getCurrency
from getData.data import getSite,getStock,getStocNum


import re
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *






application = Flask(__name__, static_url_path='', template_folder='templates')

line_bot_api = LineBotApi('9fDKzAaq/ia4Zi0yQwuTEnGM9A+vJj8aUqGE74mo1Qp6gmgs0ALwcJnGE15molA+aI8sRwyK1G67ar+cVDjvNg6lp8gBP98N3BQpqaIm4/pTS9KD1XvHq6PnRsR/UL/TYHzhv8vw3FOi/7dNwgzuPQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7d1eb6e2a43abda7b551bee1bcb0c20b')


@application.route("/")
def index():
    return render_template('index.html')

@application.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

@application.route('/statics/<path:path>')
def send_statics(path):
    return send_from_directory('statics', path)

@application.route('/_add_numbers')
def add_numbers():

    query = request.args.get('query')
    query = query.upper()
    query = re.sub('臺','台',query)
    reply = '我不知道你在說什麼'
    
    try:
        if(re.search('氣溫',query)!=None):
            regex = re.compile(getSite())
            query = regex.search(query)
            reply=getWeather(query.group(1),0)
        elif(re.search('天氣',query)!=None):
            regex = re.compile(getSite())
            query = regex.search(query)
            reply=getWeather(query.group(1),2)
        elif(re.search(getStock(),query)!=None):
            stock = getStocNum()
            regex = re.compile(getStock())
            stockname = regex.search(query)
            if (re.search('(市|買|賣|成交|收|開|高|低)',query)!=None):
                regex = re.compile('(市|買|賣|成交|收|開|高|低)')
                select ={'市':1,'買':2,'賣':3,'成交':4,'收':5,'開':6,'高':7,'低':8} 
                stockCode =regex.search(query)
                reply =  getfixstock(stock[stockname.group(0)],select[stockCode.group(0)])
            else:
                reply = getfixstock(stock[stockname.group(0)],0)
        elif(re.search('\d',query)!=None):
            regex = re.compile('\d+')
            stocknum=regex.search(query)
            if (re.search('(市|買|賣|成交|收|開|高|低)',query)!=None):
                regex = re.compile('(市|買|賣|成交|收|開|高|低)')
                select ={'市':1,'買':2,'賣':3,'成交':4,'收':5,'開':6,'高':7,'低':8} 
                stockCode =regex.search(query)
                reply =  getfixstock(stocknum.group(),select[stockCode.group(0)])
            else:
                reply = getfixstock(stocknum.group(),0)
        elif(re.search('油價',query)!=None):
            reply = getOilPrice()
    
        elif(re.search('黃金',query)!=None):
            reply = getGolden()
        elif(re.search('(美金|日圓|日元|人民幣|英鎊|歐元)',query)!=None):
            regex = re.compile('(美金|日圓|日元|人民幣|英鎊|歐元)')
            query = regex.search(query)
            reply = getCurrency(query.group(1))


        #請問本公司之續次保費繳費方式有哪些？
        elif(re.findall('續', query)!=None):
            if (re.findall('保費|保險費', query)!=None):
                if (re.findall('繳', query)!=None):
                    reply = '本公司之續次保費繳費方式：人員收費、金融機構轉帳、信用卡代繳、保戶自行繳費(如郵撥..)'

        #我收到繳費通知，但沒有人來收保費應該怎麼辦？
        elif(re.findall('沒有', query)!=None):
            if (re.findall('收', query)!=None):
                if (re.findall('保費', query)!=None):
                    reply = '1. 您可以依繳費通知上記載之收費單位地址、電話逕與收費人員連絡。 2. 您可以撥打保戶服務專線0809-000-550與本公司連絡，來電時請留下保單號碼、電話及地址，以便通知收費人員與您連絡。'
        
        #請問支票抬頭應如何開立？
        elif(re.findall('支票', query)!=None):
            if (re.findall('抬頭', query)!=None):
                reply = '本公司之續次保費繳費方式：人員收費、金融機構轉帳、信用卡代繳、保戶自行繳費(如郵撥..)'

        #我若移居國外，其收費情形應如何處理？
        elif(re.findall('國外', query)!=None):
            if (re.findall('收費', query)!=None):
                reply = '本公司在國外並未設立營業據點，無法受理保戶將收費地址變更至國外，所以保戶移居國外，仍須於國內留有收費地址，可委託國內之親友代繳或以自動轉帳、信用卡方式扣繳保費（仍須於國內設有轉帳帳戶）。'

        #我遺失送金單時，該怎麼辦？
        elif(re.findall('遺失|不見|補發', query)!=None):
            if (re.findall('送金單', query)!=None):
                if (re.findall('開立|填寫', query)!=None):
                    reply = '1.如果可以確定已繳費入帳，則送金單遺失並不影響您的保險權益。 2.如您不放心，可向保費帳務部或分公司、地區行政中心申請補發，惟補發後您不得持原送金單向本公司作任何主張。'

        #我的保單服務員是誰？
        elif(re.findall('保單', query)!=None):
            if (re.findall('服務員', query)!=None):
                reply = '富邦金控官網中的「人壽保戶會員專區」有提供保單相關資料的查詢。您必須是富邦保戶並申請加入會員，即可透過網路查詢到以您為要保人的相關保單資料。'

        

        else:
            query = query.upper()
            response = runAIML(query)
            if response != '':
                reply = response
            else:
                raise Exception
            
            
           
       
        
    except Exception as e:
        print(e)
        pass
    return jsonify(result=reply)
@application.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    application.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply = "我不知道你在說什麼"
    query = event.message.text
    query = query.upper()
    query = re.sub('臺','台',query)
    
    if(re.search('氣溫',query)!=None):
        regex = re.compile('(台北|新北|台中|高雄|台南|桃園|基隆|新竹|雲林|南投|嘉義|苗栗|彰化|花蓮|台東|澎湖|宜蘭)')
        query = regex.search(query)
        reply=getWeather(query.group(1),0)
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))
    elif(re.search('天氣',query)!=None):
        regex = re.compile('(台北|新北|台中|高雄|台南|桃園|基隆|新竹|雲林|南投|嘉義|苗栗|彰化|花蓮|台東|澎湖|宜蘭)')
        query = regex.search(query)
        reply=getWeather(query.group(1),2)
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))
    elif(re.search(getStock(),query)!=None):
        stock = getStocNum()
        regex = re.compile(getStock())
        stockname = regex.search(query)
        if (re.search('(市|買|賣|成交|收|開|高|低)',query)!=None):
            regex = re.compile('(市|買|賣|成交|收|開|高|低)')
            select ={'市':1,'買':2,'賣':3,'成交':4,'收':5,'開':6,'高':7,'低':8} 
            stockCode =regex.search(query)
            reply =  getfixstock(stock[stockname.group(0)],select[stockCode.group(0)])
        else:
            reply = getfixstock(stock[stockname.group(0)],0)
      
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))
    elif(re.search('油價',query)!=None):
        reply = getOilPrice()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))
    
    elif(re.search('黃金',query)!=None):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=getGolden()))
    elif(re.search('(美金|日圓|日元|人民幣|英鎊|歐元)',query)!=None):
        regex = re.compile('(美金|日圓|日元|人民幣|英鎊|歐元)')
        query = regex.search(query)
        reply = getCurrency(query.group(1))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))
    elif(re.search('\d',query)!=None):
        regex = re.compile('\d+')
        stocknum=regex.search(query)
        if (re.search('(市|買|賣|成交|收|開|高|低)',query)!=None):
            regex = re.compile('(市|買|賣|成交|收|開|高|低)')
            select ={'市':1,'買':2,'賣':3,'成交':4,'收':5,'開':6,'高':7,'低':8} 
            stockCode =regex.search(query)
            reply =  getfixstock(stocknum.group(),select[stockCode.group(0)])
        else:
            reply = getfixstock(stocknum.group(),0)
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))
    else:
        query = query.upper()
        response = runAIML(query)
        if response != '':
            reply = response
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))

          
if __name__ == "__main__":
    application.run()
