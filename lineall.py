from flask import Flask, send_file, send_from_directory, request, jsonify, render_template, abort
from getData.weather import getWeather
from getData.stock import getStock
from getData.petroleum import getPageSource
from getData.runAIML import runAIML
import re
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

application = Flask(__name__, static_url_path='', template_folder='templates')

line_bot_api = LineBotApi('kzgqlZeHeZ+n3djiZ0gYh4hKaCemU1dt93i4QMUXAyIdmUjDyVwqcMYsXRD2qLMtoLcVmvCDVdBdkXLNUVEW8u9M7DSit9k7Gc0gNDDzdIZuA+4lai4RFbZx1o2HronZwnDTAkSXU/nFSIg8Ed4c6wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('47752619b0088bf616337adcb9bf806')


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
    elif event.message.text == "影片":
        line_bot_api.reply_message(event.reply_token,VideoSendMessage(original_content_url='https://www.youtube.com/watch?v=osKx1pdNHAw', preview_image_url='https://www.google.com.tw/search?biw=1536&bih=734&tbm=isch&sa=1&ei=QQ3NWrHuC4ae0gTOsqWQBQ&q=%E4%BF%9D%E9%9A%AA%E5%9C%96%E7%89%87&oq=%E4%BF%9D%E9%9A%AA%E5%9C%96%E7%89%87&gs_l=psy-ab.3...3206.4069.0.4456.7.6.0.0.0.0.48.215.6.6.0....0...1c.1j4.64.psy-ab..2.0.0....0.GTImWgbrOBs#imgrc=BAt7pm7sagl6SM:'))
    elif event.message.text == "保單遺失了怎麼辦":
        Confirm_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ConfirmTemplate(
            title='這是ConfirmTemplate',
            text='請問是保單遺失要申請補發嗎?',
            actions=[                              
                PostbackTemplateAction(
                    label='是',
                    text='是',
                    data='action=buy&itemid=1'
                ),
                MessageTemplateAction(
                    label='否',
                    text='否'
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token,Confirm_template)
    elif event.message.text =='是':
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='申請補發保單，應備文件如下：1.工本費。2.契約變更申請書。'))
    elif event.message.text =='目錄':
        buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/CP0CSE3.jpg',
            title='Insurman',
            text='目錄',
            actions=[
            PostbackTemplateAction(
                label='壽險分類',
                text='壽險分類',
                data='action=buy&itemid=1'
            ),
            MessageTemplateAction(
                label='保單',
                text='保單'
            ),
            URITemplateAction(
                label='網路投保',
                uri='http://example.com/'
            ),
            PostbackTemplateAction(
                label='常見Q&A',
                text='常見Q&A',
                data='action=buy&itemid=1'
            )
        ]
    )
)
        line_bot_api.reply_message(event.reply_token,buttons_template_message)
    elif event.message.text == "壽險分類":
        Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/sHBtmhO.jpgg',
                title='住院醫療保險',
                text='1',
                actions=[
                    PostbackTemplateAction(
                        label='日額給付型',
                        text='日額給付型',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='實支實付型',
                        text='實支實付型'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/W65D0os.jpg',
                title='意外保險',
                text='2',
                actions=[
                    PostbackTemplateAction(
                        label='身故及殘廢',
                        text='身故及殘廢',
                        data='action=buy&itemid=2'
                    ),
                    MessageTemplateAction(
                        label='傷害醫療',
                        text='傷害醫療'
                    )  
                ]
            )
        ]
    )
    )
        line_bot_api.reply_message(event.reply_token,Carousel_template)
    elif event.message.text == "69大魔王":
        Image_Carousel = TemplateSendMessage(
        alt_text='目錄 template',
        template=ImageCarouselTemplate(
        columns=[
            ImageCarouselColumn(
                image_url='https://i.imgur.com/ELolpX7.jpg',
                action=PostbackTemplateAction(
                    label='postback1',
                    text='postback text1',
                    data='action=buy&itemid=1'
                )
            ),
            ImageCarouselColumn(
                image_url='https://i.imgur.com/ELolpX7.jpg',
                action=PostbackTemplateAction(
                    label='postback2',
                    text='postback text2',
                    data='action=buy&itemid=2'
                )
            )
        ]
    )
    )
        line_bot_api.reply_message(event.reply_token,Image_Carousel)
    elif event.message.text == "你好":
        buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/mobSkDW.jpg',
            title='Insurman',
            text='請問使用者需要什麼服務?',
            actions=[
            PostbackTemplateAction(
                label='保險Q&A',
                text='保險Q&A',
                data='action=buy&itemid=1'
            ),
            PostbackTemplateAction(
                label='閒聊功能',
                text='閒聊功能',
                data='action=buy&itemid=1'
            ),
            PostbackTemplateAction(
                label='說個笑話',
                text='說個笑話',
                data='action=buy&itemid=1'
            )
            
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token,buttons_template_message)
    elif event.message.text == "保險Q&A":
         line_bot_api.reply_message(
         event.reply_token,
         TextSendMessage(text='使用者可以輸入以下格式：\n 1.請問「名詞」的「名詞」如何「動詞」\n 2.請問「名詞」的「名詞」是否「動詞」\n範例：\n1. 請問遺失的保單如何補辦\n2. 請問遺失的保單是否能夠補辦'))      
    elif event.message.text == "閒聊功能":
         line_bot_api.reply_message(
         event.reply_token,
         TextSendMessage(text='那我們來聊天吧')) 
    elif event.message.text == "說個笑話":
         line_bot_api.reply_message(
         event.reply_token,
         TextSendMessage(text='小明爬到2樓，為何覺得腿很酸?\n因為他踩到檸檬'))
         
         
    elif re.findall('續',event.message.text)[0]:
        if re.findall('保費',event.message.text)[0]:
            if re.findall('繳費',event.message.text)[0]:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='本公司之續次保費繳費方式：人員收費、金融機構轉帳、信用卡代繳、保戶自行繳費(如郵撥..)'))

       
    else:
        query = query.upper()
        response = runAIML(query)
        if response != '':
            reply = response
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))  

if __name__ == "__main__":
    application.run()
