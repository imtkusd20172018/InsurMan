
# coding: utf-8

# In[9]:


from flask import Flask, send_file, send_from_directory, request, jsonify, render_template, abort
from getData.weather import getWeather
from getData.stock import getStock
from getData.petroleum import getPageSource
from getData.runAIML import runAIML
import re
import random

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
    elif re.findall('笑話',event.message.text):
        #笑話
        list1 = ['什麼東西可以攔截電子？', '玻璃跳樓之前會說什麼？', '小明是個很愛挖人屁股的死小孩，看到有人在他前面就會情不自禁的戳人屁股，戳完就哈哈大笑的跑走，非常的白目。有一天小明看到阿胖，目標顯眼龐大，便神不知鬼不覺的跑道阿胖後面，用力的往小胖屁眼捅下去，結果好死不死，阿胖其實急著要去上大號，就這樣受到驚嚇的阿胖，屎就這麼從小明手上給噴了出來。這時老師衝了出來，不斷安撫失禁後哭泣的阿胖，並叫同學拿一件新的褲子先給阿胖穿。結果頭一轉發現小明表情痛苦地倒在那邊，不知道發生了什麼事情，於是老師問小明：怎麼了？表情這麼痛苦只見小明全身顫抖表情十分猙獰，顫抖的對著老師說：']
        list2 = ['「紅橙黃綠」', '「晚安，因為它要睡了」', '「我剛剛嚇到吃手手了」']

<<<<<<< HEAD
    x = random.randint(0,2)

    if re.findall('笑話',event.message.text)  == '笑話':
=======
        x = random.randint(0,2)
>>>>>>> 97af119118dd8ba825f4dd1c69ce1296255f24b3
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(list1[x]+"\n"+list2[x]))
            
    
    #請問本公司之續次保費繳費方式有哪些？     
<<<<<<< HEAD
    elif re.findall('續',event.message.text)  == '續':
        if re.findall('保費|保險費',event.message.text)[0] == '保費|保險費':
            if re.findall('繳',event.message.text)[0] == '繳':
=======
    elif re.findall('續',event.message.text):
        if re.findall('保費|保險費',event.message.text):
            if re.findall('繳',event.message.text):
>>>>>>> 97af119118dd8ba825f4dd1c69ce1296255f24b3
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='本公司之續次保費繳費方式：人員收費、金融機構轉帳、信用卡代繳、保戶自行繳費(如郵撥..)'))
                
    #我收到繳費通知，但沒有人來收保費應該怎麼辦？
    elif re.findall('沒有',event.message.text):
        if re.findall('收',event.message.text):
            if re.findall('保費',event.message.text):
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='1. 您可以依繳費通知上記載之收費單位地址、電話逕與收費人員連絡。 2. 您可以撥打保戶服務專線0809-000-550與本公司連絡，來電時請留下保單號碼、電話及地址，以便通知收費人員與您連絡。'))

    #請問支票抬頭應如何開立？
    elif re.findall('支票',event.message.text):
        if re.findall('抬頭',event.message.text):
            if re.findall('開立|填寫',event.message.text):
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='支票抬頭請依下列方式填寫： 1. 富邦人壽。 2. 富邦人壽保險（股）公司。 3. 富邦人壽保險股份有限公司。'))
                
    #我若移居國外，其收費情形應如何處理？
    elif re.findall('國外',event.message.text):
        if re.findall('收費',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='本公司在國外並未設立營業據點，無法受理保戶將收費地址變更至國外，所以保戶移居國外，仍須於國內留有收費地址，可委託國內之親友代繳或以自動轉帳、信用卡方式扣繳保費（仍須於國內設有轉帳帳戶）。'))     
        
        
    #我遺失送金單時，該怎麼辦？
    elif re.findall('遺失|不見|補發',event.message.text):
        if re.findall('送金單',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='1.如果可以確定已繳費入帳，則送金單遺失並不影響您的保險權益。 2.如您不放心，可向保費帳務部或分公司、地區行政中心申請補發，惟補發後您不得持原送金單向本公司作任何主張。'))     
        

    #我的保單服務員是誰？
    elif re.findall('保單',event.message.text):
        if re.findall('服務員',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='富邦金控官網中的「人壽保戶會員專區」有提供保單相關資料的查詢。您必須是富邦保戶並申請加入會員，即可透過網路查詢到以您為要保人的相關保單資料。'))     
        

    #要保人由甲變更為乙時，其應注意事項及檢附文件為何？
    elif re.findall('要保人',event.message.text):
        if re.findall('變更',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='您詢問的險種有分成「傳統型」及「投資型」，請加入險種類型再詢問一次。'))
            
    elif re.findall('傳統型',event.message.text):
        if re.findall('要保人',event.message.text):
            if re.findall('變更',event.message.text):
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='應檢附之文件：(1) 契約變更申請書。 (2) 公司登記證明文件或商業登記證明文件。 (3) 證明文件（足以辨識要、被保人關係及是否具“保險利益”）。')) 
            
    elif re.findall('投資型',event.message.text):
        if re.findall('要保人',event.message.text):
            if re.findall('變更',event.message.text):
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='應注意事項： 要保人變更為該保單所有權利義務之移轉，必須由原要保人親自提出申請並經被保險人同意；故本項變更申請，務必由原要保人及被保險人親自填立『契約變更申請書』並簽章。變更後之要保人應對被保險人之生命身體具“保險利益”，並提供足以證明其關係之證明文件。依保險法第十六條規定，要保人對下列各人之生命或身體，有“保險利益”： A.本人或其家屬。B.生活費或教育費所仰給之人。C.債務人。D.為本人管理財產或利益之人。要保人變更時，應注意要保人地址及受益人是否須同時辦理變更。'))            
            
        
    #要、被保人非同一人，要保人不幸死亡，應如何變更要保人？
    elif re.findall('要保人',event.message.text):
        if re.findall('死亡',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='原要保人死亡時，該保險契約視同要保人之遺產，應由其繼承人中推舉一與被保險人具“保險利益”（依保險法第十六條規定）者繼承該保單。應備文件如下：(1) 契約變更申請書。 (2) 原要保人死亡證明或除戶證明。 (3) 全部戶籍謄本（以認定其所有繼承人）。 (4) 法定繼承人聲明同意書：原要保人之所有法定繼承人，一一於同意書親自簽章，以聲明同意讓受該保險契約由所指定之新要保人持有。'))     

        
    #保險單上要保人或被保險人姓名、出生日期、性別或身分證號碼錯誤時，應如何處理？
    elif re.findall('錯誤',event.message.text):
        if re.findall('姓名|生日|姓別|身分證|資料',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='要保書填載錯誤：(1) 請檢附契約變更申請書及證明文件，依變更程序辦理。 (2) 出生日期更正，如涉及保險年齡異動，則依變更後保險年齡重新計算保險費，並依保單條款規定補退保費差額；變更後契約內容依投保規定辦理。(3) 性別更正，依變更後性別重新計算保險費，並補退保費差額。'))   
        
        
    #要保人（或被保險人）更改名時，應如何處理？
    elif re.findall('更改|變更|更|改',event.message.text):
        if re.findall('姓名|名',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='1. 請檢附契約變更申請書及戶籍謄本，依變更程序辦理。 2. 於要保人（或被保險人）簽章處簽立原姓名（即要保書原留樣式）及更改後之姓名。'))   

    
    #保險費自動墊繳意願應如何變更？    
    elif re.findall('保費|保險費',event.message.text):
        if re.findall('自動墊繳意願',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='1. 隨時均可提出申請，但若保單已進入自動墊繳，現欲變更為停止保險費自動墊繳，則墊繳意願變更之生效日為次一墊繳日。 2. 應備妥「契約變更申請書」，由要保人提出申請。'))

    #被保險人職業內容變動該如何辦理？
    elif re.findall('職業|工作',event.message.text):
        if re.findall('更改|變更|變動|換',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='被保險人之實際工作內容有變動時，保戶應即時以書面通知保險公司，填寫契約變更申請書辦理變更。'))


    #如何辦理地址之變更？
    elif re.findall('地址|住址',event.message.text):
        if re.findall('更改|變更|變動|換',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='收費地址之變更，可以下列方式辦理： 1. 要保人填寫契約變更申請書，逕寄總公司或當地服務中心辦理。 2. 變更後地址不得為郵政信箱。'))


    #受益人可否變更？應如何申請？
    elif re.findall('受益人',event.message.text):
        if re.findall('更改|變更|變動|換',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='1. 在保險事故未發生前可受理變更；由要保人提出申請，經被保險人親自簽章同意。應備文件如下： (1)契約變更申請書  2. 應注意事項： (1) 原則上以與被保險人具保險利益者為限。 (2) 如指定之受益人為其他人，則應註明其姓名、身分證號碼、與被保險人之關係。 (3) 若受益人有二位以上，則需寫明保險金分配方式，如順位、比例、均分。 (4) 受益人為慈善機構，需註明統一編號與地址。 (5) 若受益人與被保險人無血親關係（如同居人），請填寫身分證字號及戶籍地址。'))

    #保戶欲辦理變更為「減額繳清保險」應如何辦理？
    elif re.findall('減額繳清保險',event.message.text):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='1. 要保人繳足保險費累積達有保單價值準備金時，始可提出辦理。 2. 應備文件如下：契約變更申請書。 3. 應注意事項如下： (1) 如有未兌現支票，則須先換現，或待支票兌現後才予以辦理。 (2) 主契約辦理變更時，附約則依契約條款約定處理。 (3) 各險種可否變更，依各契約條款約定處理。 (4) 變更為減額繳清保險後，要保人不必再繳保險費，該契約繼續有效，但保險金額以減額繳清保險金額為準。 (5) 契約變更為「減額繳清保險」後，本公司不再接受保險金額及險種之變更。'))

    
    #保戶欲辦理變更為「展期定期保險」應如何辦理？
    elif re.findall('展期定期保險',event.message.text):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='1. 要保人繳足保險費累積達有保單價值準備金時，始可提出辦理。 2. 應備文件如下：契約變更申請書。 3. 應注意事項如下： (1) 如有未兌現支票，則須先換現，或待支票兌現後才予以辦理。 (2) 主契約辦理變更時，附約則依契約條款約定處理。 (3) 各險種可否變更，依各契約條款約定處理。 (4) 變更為展期定期保險後，其保險金額為當年度保險金額扣除保險單借款本息或墊繳保險費本息後之餘額，要保人不必再繳保險費。 (5) 契約變更為「展期定期保險」後，本公司不再接受保險金額及險種之變更。'))
    
    
    #辦理繳別變更，應備什麼文件及注意事項？    
    elif re.findall('繳別',event.message.text):
        if re.findall('更改|變更|變動|換',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='1. 填寫保險契約內容變更申請書，可隨時辦理。 2. 在契約繳費期間內，可申請變更為年繳、半年繳、季繳或月繳。 3. 變更後月繳件之繳費方式須為轉帳件、信用卡件或自行繳費件。'))
    

    #何謂繳費方式變更？
    elif re.findall('繳費|繳費方式',event.message.text):
        if re.findall('更改|變更|變動|換',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='即繳交保費之方式與管道：轉帳件、信用卡件、自行繳費件。應備文件如下： 1. 變更為自行繳費件：終止付款申請書、信用卡/自行繳費付款授權書。2. 變更為轉帳件：金融機構付款授權書。 3. 變更為信用卡件：信用卡/自行繳費付款授權書。'))
        
        
    #保單遺失如何申請補發？
    elif re.findall('保單|保險單',event.message.text):
        if re.findall('遺失|不見|補發',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='申請補發保單，應備文件如下： 1. 工本費。 2. 契約變更申請書。'))
        
    #主契約保險金額之縮小應如何提出申請？
    elif re.findall('保險|保費',event.message.text):
        if re.findall('金額',event.message.text):
            if re.findall('縮小',event.message.text):
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='1. 應備文件如下：契約變更申請書。 2. 注意事項如下： (1) 縮小部份視同終止契約，契約累積達有解約金時，按其終止部份核算解約金返還要保人；如契約繳費未有解約金時，則無須退還任何費用。 (2) 縮小後保額不得低於該險種最低承保限額；且附約之投保限額須符合投保規則。 (3) 原契約若有貸款未清償，而貸款金額超過縮小保額後之最高可貸金額時，則超貸部份之本息應作還款清償。 (4) 已辦理「減額繳清保險」、「展期定期保險」者，不得再申請縮小主約保額。'))
    
    #要保人於契約每屆滿五週年日或於被保險人結婚或其子女出生後之第一個契約週年日提出主契約保險金額之增加權，應備文件及注意事項為何？
    
    #投保當時如無附加一年期附約，中途可否附加？
    elif re.findall('無|沒有',event.message.text):
        if re.findall('附約',event.message.text):
            if re.findall('中途',event.message.text):
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='視主約險種附加附約規定。（部分主約限定不得附加附約）'))
                    
    #保戶若申請附約取消或縮小保額時，可否退費？
    elif re.findall('附約',event.message.text):
        if re.findall('取消|中止|停止|縮小',event.message.text):
            if re.findall('退費',event.message.text):
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='1. 癌症險附約或一年期附約之取消或縮小保額時，係按日數比例退還未經過期間保費。 2. 長年期壽險附約之取消或縮小保額時，如有解約金，則退還解約金差額；如未累積有解約金，則不返還任何費用。'))
                    
    #保戶若申請附約新加保，應如何辦理？
    elif re.findall('無|沒有',event.message.text):
        if re.findall('附約',event.message.text):
            if re.findall('中途',event.message.text):
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='1. 應備文件如下： (1) 契約變更申請書 (2) 健康聲明書 2. 在契約有效期間內之任何時間，可新增購本公司仍繼續銷售之附約產品，保險費按要保人新加保附約時之投保年齡計算。（需補繳新購附約產品保費） 3. 申請眷屬附加時，變更申請書及健康聲明書除要被保險人須簽名外，亦應取得眷屬被保險人簽名，如未滿20足歲時，需其法定代理人簽名同意 4. 新加保商品申請，仍須經由本公司風險審核通過。 5. 新加保商品申請需於審核通過且繳費後生效，生效日契約追溯原申請日。 6. 附約保障年期不得大於主約保障年期。'))
                    
    #契約轉換應備哪些文件？
    #主契約可轉換之作業與險種規定為何？
    elif re.findall('契約',event.message.text):
        if re.findall('轉換|更改|變更|變動|換',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='1. 保險契約滿一週年後，可依公司規定申請契約變更為公司仍繼續銷售之壽險保險契約。 2. 變更後保險金額不得低於本公司對該險種的最低承保金額，且變更後契約的當年度危險保額不得高於原契約變更當年度的危險保額。 3. 應備文件如下：(1) 契約變更申請書。 (2) 健康聲明書。 (3) 被保險人未滿14歲者應檢附『批註條款及除外聲明事項』。 (4) 險種轉換暨年期變更利益比較表。'))
        
    #什麼情形不得申請轉換契約？
    elif re.findall('不能|不得|不行|不可以|失敗',event.message.text):
        if re.findall('轉換|更改|變更|變動|換',event.message.text):
            if re.findall('契約',event.message.text):
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='1. 停效件須先辦理復效。 2.已變更為展期或減額繳清保險者。 3. 繳費期滿件或躉繳件。 4. 已享有豁免保費者。'))
                    
    #轉換後契約之投保始期與保險年齡如何計算？
    elif re.findall('轉換|更改|變更|變動|換',event.message.text):
        if re.findall('契約',event.message.text):
            if re.findall('年齡|時間|始期',event.message.text):
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='轉換後契約之投保始期與計算保險費的年齡與原契約相同。'))
    
    #申請保險年期變更，應備哪些文件？
    #年期變更之規定為何？
    elif re.findall('年期',event.message.text):
        if re.findall('轉換|更改|變更|變動|換',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='1. 申請年期變更者契約須持續有效一年以上，可依公司規定申請辦理年期變更。 2. 附約之保險期間不得超過主契約之保險期間。 3. 變更後契約的當年度危險保額不得高於原契約變更當年度的危險保額。 4. 應備文件如下： (1) 契約變更申請書(繁式)。 (2) 健康聲明書（延長年期時檢附）。 (3) 險種轉換暨年期變更利益比較表。'))
                
    #契約「停效」後，該如何申請復效？
    elif re.findall('契約',event.message.text):
        if re.findall('復效',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='1. 應備文件如下： (1) 契約變更申請書。 (2) 停效超過6個月時應檢附： (A)健康聲明書。 (B)體檢報告書及其收據。 (C)復效件預先審查申請單。 2. 應注意事項如下： (1) 停效二年內之契約方可提出復效申請。 (2) 如有貸款，亦須同時繳交累積之貸款利息。 (3) 申請契約復效，需經本公司同意，並經要保人清償欠繳保險費扣除停效期間危險保費的餘額，自翌日上午零時起恢復效力。'))            
    
    #如何辦理國外理賠件？
    elif re.findall('國外',event.message.text):
        if re.findall('理賠',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='1. 所就診之醫院、診所，必須是當地政府正式註冊，領有執照者，且必須符合條款及醫療法之規定。 2. 國外理賠件如發生於非美語國家，請事先將相關資料及單據內容翻譯，再行送件 。 3.大陸地區就診文件，需依政府規定至相關單位公證'))
                
    #失能診斷書和一般診斷書有何不同？
    #一般理賠之申請，可否以影本診斷書提出申請？
    elif re.findall('診斷書',event.message.text):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='1. 一般診斷書主要記載就診期間及其傷（病）情等；而失能診斷書則須詳述其缺失或機能喪失之狀況，有否恢復之可能以及有否達失能之程度。 2. 申請理賠一律以正本診斷書為原則，若係影本診斷書者，保戶可請醫院於影本加蓋關防，如此便可代替正本使用。'))
    
    #請問若事故者為未成年人，其理賠申請書及同意查詢聲明書應如何填寫才對呢？
    elif re.findall('未成年',event.message.text):
        if re.findall('理賠|申請書',event.message.text):
            if re.findall('填寫|申請',event.message.text):
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='在理賠申請書下方之立書人(即被保險人)/受益人簽章部分由事故者本人親自簽名(章)，不能親自為之者由父母代簽。右方之法定代理人則均須由父母簽章即可(同意查詢聲明書亦同)，此為填寫理賠申請書之正確方式。'))
                    
    #被保險人死亡，受益人未成年，應如何提出申請理賠？
    elif re.findall('死亡',event.message.text):
        if re.findall('受益人',event.message.text):
            if re.findall('未成年',event.message.text):
                if re.findall('理賠',event.message.text):
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='受益人未滿七歲者，由其法定代理人簽章提出申請；滿七歲以上者除簽章外，其法定代理人亦須簽章協同提出申請。'))
    
    #住院日數如何計算？
    elif re.findall('住院',event.message.text):
        if re.findall('日數|天數',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='住院日數之計算採計頭計尾，例如1/1入院至1/3出院，住院日數為3天。'))
    
    #當日出院後於當天又再度入院，住院天數算幾天？
    elif re.findall('出院',event.message.text):
        if re.findall('又|再',event.message.text):
            if re.findall('住院',event.message.text):
                if re.findall('日數|天數',event.message.text):
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='仍算一天。'))
    
    #包皮過長去醫院切除並住院，可否理賠？
    elif re.findall('包皮',event.message.text):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='若有合併發炎情形則可給付。')) 
                
    #收據遺失是否可以副本或補發收據代替申請？
    elif re.findall('收據',event.message.text):
        if re.findall('遺失|不見|補發',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='副本收據或補發收據不可代替正本收據申請理賠。'))  
                
    #中醫診所住院治療，其理賠給付準則如何？
    elif re.findall('中醫',event.message.text):
        if re.findall('住院',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='1. 依醫療法第１１條：「醫療機構設有病房收治病人者為醫院，僅門診者為診所，非以直接診治病人為目的而由醫師辦理醫療保健業務之機構為其他醫療機構。前項診所得設置九張以下之觀察病床......」 2. 中醫診所非條款所定義之住院醫院，故凡保戶於中醫診所住院申請住院醫療保險金時，依規定均不符合給付條件。'))             
                
    #吃蝦子因不慎吞入蝦殼，因而刺傷食道，是否算是意外？
    elif re.findall('蝦子',event.message.text):
        if re.findall('刺傷',event.message.text):
            if re.findall('食道',event.message.text):    
                if re.findall('意外',event.message.text):
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='是。'))            

                        
    #被電電擊到而受傷是否可申請意外傷害醫療保險金？
    elif re.findall('電|電擊',event.message.text):
        if re.findall('意外',event.message.text):  
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='若可排除自致之行為，則可申請意外傷害醫療保險金。'))                            
                        
    #事故人被人砍傷，是否可給付？
    elif re.findall('砍|砍傷',event.message.text):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='若可排除除外責任則可給付。'))                            
                        
    #中暑是否可申請意外傷害醫療保險金？
    elif re.findall('中暑',event.message.text):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='不符意外險條款約定之條件，不給付。'))             
    
            
    #食物中毒，是否屬傷害醫療險範圍？可否給付？
    elif re.findall('食物中毒',event.message.text): 
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='1. 食物中毒若係被保險人本身體質所致者，（如食物過敏、腸胃不好等），則非屬傷害範圍。 2. 若為集體性中毒（需三人以上），可証明係外來突發之不可抗力事故，則可依約核付。'))            
                        
    #分娩死亡是否屬意外死亡？ 
    elif re.findall('分娩',event.message.text):
        if re.findall('死亡',event.message.text):  
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='分娩死亡並非外來傷害所致，故不屬意外死亡。'))            
            
    #腰椎間盤突出症傷害醫療附約是否皆不予給付？
    elif re.findall('椎間盤突出',event.message.text):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='腰椎間盤突出症一般而言皆為內發性疾病，但有時亦有可能為外來的傷害所致，如動力撞擊或高處墜落而導致腰椎間盤突出症，惟是否合於傷害理賠要件，完全依其案情是否有足資認定為外來之意外傷害所造成而定。'))               
    
            
    #良性腫瘤是否可申請癌症保險金？
    elif re.findall('良性腫瘤',event.message.text):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='良性腫瘤非癌症不符合癌症保險金給付條件。'))             
                   
    #若保戶為醫師，申請癌症保險金有無特別限制？        
    elif re.findall('要保人|被保人|受益人|保戶',event.message.text):
        if re.findall('醫生|醫師',event.message.text):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='依契約條款規定要保人、被保人或受益人為醫師者，所開具被保人有關癌症的診斷證明，不得作為申請保險金的文件。特別說明事項：公司自96.11.01起所開辦之新商品依循「住院醫療費用保險單示範條款」，故條款中針對保險金的申領應檢具文件之醫療診斷書或住院證明，有載明：......如要保人或被保險人為醫師時，不得為被保險人出具診斷書或住院證明，應依此約定辦理；惟條款未載明者仍依原條款約定辦理。'))             
    
    
    #被保險人飲酒後駕(騎)車所發生之事故，在理賠給付上之認定為何？            
    elif re.findall('酒',event.message.text):
        if re.findall('駕',event.message.text):
            if re.findall('理賠',event.message.text):    
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='依意外傷害失能保險附約之除外責任：被保險人飲酒後駕(騎)車，其吐氣或血液所含酒精成份超過道路交通法令規定標準者，不負給付保險金之責。若被保險人為前項所致之意外事故，本公司可不負給付之責。'))                
    
    #若保戶因心肌梗塞而死亡，但死亡診斷書上醫師勾註為意外死亡，是否能申請意外身故理賠？
    elif re.findall('心肌梗塞',event.message.text):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='心肌梗塞死亡為疾病死亡，非意外死亡，所以無法請領意外身故理賠。')) 
                    
    #保戶出外釣魚後即告失蹤，請問是否可請領死亡保險金？
    #若失蹤者為80歲以上者，是否仍須等七年？
    #若因重大災難(如水災)而失蹤者，須等幾年？        
    elif re.findall('失蹤',event.message.text):   
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='1. 依民法第8條之規定一般失蹤須等七年，且經死亡宣告者才可請領死亡保險金。 2. 80歲以上者失蹤等三年即可。 3. 重大災難失蹤期間為一年。'))                
    
    #失蹤期間是否仍需繳交保費？                
    elif re.findall('失蹤',event.message.text):
        if re.findall('繳',event.message.text):
            if re.findall('保費|保險費',event.message.text):    
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='是，失蹤期間仍需繳交保費以維持契約之有效。'))                         

    #被保人因疾病或意外成為植物人時，如何申請完全失能保險金？                
    elif re.findall('植物人',event.message.text):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='受益人為禁治產人、心神喪失或精神耗弱致不能處理自己事務者，除須檢附失能診斷書外，請檢附法院禁治產裁定書及裁定登記後之法定監護人戶籍謄本，由法定監護人簽名協助申請，理賠金之受款人仍為被保險人本人。'))                 
                    
    
    #何謂法定繼承人？        
    elif re.findall('法定繼承人',event.message.text):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='依民法第1138條之規定，配偶為當然繼承人，其次依序如下：一、直系血親卑親屬。二、父母。三、兄弟姊妹。四、祖父母。'))
             
            
    else:
        query = query.upper()
        response = runAIML(query)
        if response != '':
            reply = response
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))  

if __name__ == "__main__":
    application.run()

