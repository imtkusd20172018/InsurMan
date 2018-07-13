from flask import Flask, send_file, send_from_directory, request, jsonify, render_template, abort
from getData.weather import getWeather
from getData.runAIML import runAIML
from getData.stock2 import getfixstock
from getData.oilPrice import getOilPrice
from getData.golden import getGolden
from getData.Currency import getCurrency


import re
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests
from bs4 import BeautifulSoup






application = Flask(__name__, static_url_path='', template_folder='templates')

line_bot_api = LineBotApi('sewtf6NLPZE0f8NorguLvxk5wct9U4Xw8w57OU0JWERPBR4gf4JMs04SoE6h9iZeoLcVmvCDVdBdkXLNUVEW8u9M7DSit9k7Gc0gNDDzdIbGqvLNS/qdCf/6v0jvNd8uyhL51trPQFd8iK27I4LSCQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1ffcef0d3b851a30786de461f14f1d70')


@application.route("/")
def index():
    return render_template('index.html')

@application.route("/en")
def index_eng():
    return render_template('index_eng.html')

@application.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

@application.route('/statics/<path:path>')
def send_statics(path):
    return send_from_directory('statics', path)

@application.route('/_add_numbers')
def add_numbers():
    query = request.args.get('query')
    reply = '我不知道你在說什麼'
    try:
        if '天氣如何' in query:
            reply = '現在氣溫是' + getWeather()
        elif '我美嗎' in query:
            reply = '你好美'
        elif '我肚子好餓' in query:
            reply = '趕快去吃飯吧'
        elif '股票' in query:
            query = re.split('股票|的',query)
            code =  query[1]
            query = query[2]
            reply = getfixstock(code, query)
        elif '油價' in query:
            reply = getOilPrice()
        elif '黃金價'in query:
            reply = getGolden()
        elif '匯率' in query:
            query=re.split('匯率',query)
            c=query[0]
            reply = getCurrency(c)
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
    if '天氣' in query :
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='現在氣溫是'+getWeather()))
    elif '我好美' in query :
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='你好美'))
    elif '好餓' in query :
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='快去吃飯'))
    elif '股票' in query :
        query=re.split('股票|的',query)
        code =  query[1]
        query = query[2]
        reply = getfixstock(code, query)
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))
    elif '油價' in query :
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=getOilPrice()))
    elif '黃金價' in query:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=getGolden()))
    elif '匯率' in query:
        query=re.split('匯率',query)
        c=query[0]
        reply = getCurrency(c)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))
    elif '幹你娘' in query :
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='別說髒話啦'))        
    else:
        query = query.upper()
        response = runAIML(query)
        if response != '':
            reply = response
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))

          
if __name__ == "__main__":
    application.run()
