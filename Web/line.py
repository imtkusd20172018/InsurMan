from flask import Flask, send_file, send_from_directory, request, jsonify, render_template, abort
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
        

        #請問本公司之續次保費繳費方式有哪些？
        if(re.search('續', query)!=None):
            if (re.search('保費|保險費', query)!=None):
                if (re.search('繳', query)!=None):
                    reply = '本公司之續次保費繳費方式：人員收費、金融機構轉帳、信用卡代繳、保戶自行繳費(如郵撥..)'

        #我收到繳費通知，但沒有人來收保費應該怎麼辦？
        elif(re.search('沒有', query)!=None):
            if (re.search('收', query)!=None):
                if (re.search('保費', query)!=None):
                    reply = '1. 您可以依繳費通知上記載之收費單位地址、電話逕與收費人員連絡。 2. 您可以撥打保戶服務專線0809-000-550與本公司連絡，來電時請留下保單號碼、電話及地址，以便通知收費人員與您連絡。'
        
        #請問支票抬頭應如何開立？
        elif(re.search('支票', query)!=None):
            if (re.search('抬頭', query)!=None):
                reply = '本公司之續次保費繳費方式：人員收費、金融機構轉帳、信用卡代繳、保戶自行繳費(如郵撥..)'

        #我若移居國外，其收費情形應如何處理？
        elif(re.search('國外', query)!=None):
            if (re.search('收費', query)!=None):
                reply = '本公司在國外並未設立營業據點，無法受理保戶將收費地址變更至國外，所以保戶移居國外，仍須於國內留有收費地址，可委託國內之親友代繳或以自動轉帳、信用卡方式扣繳保費（仍須於國內設有轉帳帳戶）。'

        #我的保單服務員是誰？
        elif(re.search('保單', query)!=None):
            if (re.search('服務員', query)!=None):
                reply = '富邦金控官網中的「人壽保戶會員專區」有提供保單相關資料的查詢。您必須是富邦保戶並申請加入會員，即可透過網路查詢到以您為要保人的相關保單資料。'
        
        #要、被保人非同一人，要保人不幸死亡，應如何變更要保人？
            elif(re.search('要保人', query)!=None):
                if (re.search('死亡', query)!=None):
                        reply = '原要保人死亡時，該保險契約視同要保人之遺產，應由其繼承人中推舉一與被保險人具“保險利益”（依保險法第十六條規定）者繼承該保單。應備文件如下：(1) 契約變更申請書。 (2) 原要保人死亡證明或除戶證明。 (3) 全部戶籍謄本（以認定其所有繼承人）。 (4) 法定繼承人聲明同意書：原要保人之所有法定繼承人，一一於同意書親自簽章，以聲明同意讓受該保險契約由所指定之新要保人持有。'
        #保險單上要保人或被保險人姓名、出生日期、性別或身分證號碼錯誤時，應如何處理？
            elif(re.search('錯誤', query)!=None):
                if (re.search('姓名|生日|姓別|身分證|資料', query)!=None):
                    reply = '要保書填載錯誤：(1) 請檢附契約變更申請書及證明文件，依變更程序辦理。 (2) 出生日期更正，如涉及保險年齡異動，則依變更後保險年齡重新計算保險費，並依保單條款規定補退保費差額；變更後契約內容依投保規定辦理。(3) 性別更正，依變更後性別重新計算保險費，並補退保費差額。'
        #要保人（或被保險人）更改名時，應如何處理？
            elif(re.search('更改|變更|更|改', query)!=None):
                if (re.search('姓名|名', query)!=None):
                    reply = '1. 請檢附契約變更申請書及戶籍謄本，依變更程序辦理。 2. 於要保人（或被保險人）簽章處簽立原姓名（即要保書原留樣式）及更改後之姓名。'
        #保險費自動墊繳意願應如何變更？
            elif(re.search('保費|保險費', query)!=None):
                if (re.search('自動墊繳意願', query)!=None):
                    reply = '1. 隨時均可提出申請，但若保單已進入自動墊繳，現欲變更為停止保險費自動墊繳，則墊繳意願變更之生效日為次一墊繳日。 2. 應備妥「契約變更申請書」，由要保人提出申請。'
        #被保險人職業內容變動該如何辦理？
            elif(re.search('職業|工作', query)!=None):
                if (re.search('更改|變更|變動|換', query)!=None):
                    reply = '被保險人之實際工作內容有變動時，保戶應即時以書面通知保險公司，填寫契約變更申請書辦理變更。'
        #如何辦理地址之變更？    

        #受益人可否變更？應如何申請？

        #保戶欲辦理變更為「減額繳清保險」應如何辦理？

        #保戶欲辦理變更為「展期定期保險」應如何辦理？

        #辦理繳別變更，應備什麼文件及注意事項？    

        #何謂繳費方式變更？

        #保單遺失如何申請補發？

        #主契約保險金額之縮小應如何提出申請？

        #投保當時如無附加一年期附約，中途可否附加？

        #保戶若申請附約取消或縮小保額時，可否退費？

        #保戶若申請附約新加保，應如何辦理？

        #主契約可轉換之作業與險種規定為何？

        #什麼情形不得申請轉換契約？
            
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


          
if __name__ == "__main__":
    application.run()
