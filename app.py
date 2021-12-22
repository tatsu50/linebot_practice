from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,ImageMessage,ImageSendMessage
)
import os
import json
import random
# import urllib.request
# from bs4 import BeautifulSoup

app = Flask(__name__)

# チャネルシークレットを設定
YOUR_CHANNEL_SECRET = "c7217edc98bba84efb0036e6a8397999"
# チャネルアクセストークンを設定
YOUR_CHANNEL_ACCESS_TOKEN = "/8iYaBv+iAgEAP+6zYtHCYxMzb7uxVpiHnykssLGwa2tEtDmF9UNJeKkKyiREWwbbBG8c166Q31cvs1Xo42/gbQabK0FyM0fHCt8cRDVeGaVxQVzHz+u2+MBJshRSMJlwZX2GX+NUrZ/lPmYr22HggdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# https://example.herokuapp.com/callback にアクセスされたら以下の関数を実行する
@app.route("/callback", methods=['POST'])
def callback():
    # アクセス時に送られてきたデータ「X-Line-Signature」を代入
    signature = request.headers['X-Line-Signature']

    # アクセス時に送られてきたデータの主な部分を代入
    body = request.get_data(as_text=True)

    # try 内でエラーが発生したら except の文を実行
    try:
        # ハンドラーに定義されている関数を呼び出す
        handler.handle(body, signature)
    # もし「InvalidSigunatureError」というエラーが発生したら、以下のプログラムを実行
    except InvalidSignatureError:
        # リクエストを送った側に400番(悪いリクエストですよー！)を返す
        abort(400)

    # すべて順調にいけば、リクエストを送った側に「OK」と返す
    return "OK"

# ハンドラーに定義されている関数
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ここにメッセージの内容による処理を書いていこう

    # メッセージの種類が「テキスト」なら
    if event.type == "message":
        responses = []
        response_message = ""
        response_image =""

        # event.message.text という変数にメッセージの内容が入っている
        if (event.message.text == "おはようございます"):
            response_message = "Good morning!"
            response_message =""
        elif (event.message.text == "こんにちは"):
            response_message = "Good afternoon!"

        elif (event.message.text == "こんばんは"):
            response_message = "Good evening!"

        elif (event.message.text == "コンター図"):
            response_message = "今日の図"
            response_image ="https://web19231.azurewebsites.net/pbl/img/FPS.jpg"
            # return client.replyMessage(event.replyToken, {
            #     type: 'image',
            #     originalContentUrl: 'オリジナルサイズの画像URL', 
            #     previewImageUrl: 'https://web19231.azurewebsites.net/pbl/img/FPS.jpg'
            # })
            responses.append(
                ImageSendMessage(
                    original_content_url=response_image,
                    preview_image_url=response_image
                )
            )

        else:
            response_message = "その言葉はわかりません。"
        
        responses.append(
            TextMessage(text=response_message)
        )

        # 返信文を送信
        # response_message の中に入っている文を返す
        # line_bot_api.reply_message(
        #     event.reply_token,
        #     [   
        #         TextMessage(text=response_message),
        #         ImageSendMessage(
        #             original_content_url=response_image,
        #             preview_image_url=response_image
        #         )
        #     ]
        # )
        line_bot_api.reply_message(
            event.reply_token,
            responses
        )

# @handler.add(MessageEvent,message=TextMessage)
# def handle_message(event):
#     #入力された文字を取得
#     text_in = event.message.text

#     if "今日" in text_in:#scw.pyのgetw関数を呼び出している
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text=scw.getw()))
#     elif "明日" in text_in:#scw.pyのtom_getw関数を呼び出している
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text=scw.tom_getw()))
#     else:
#         response_message = "その言葉はわかりません。"

# ポート番号を環境変数から取得
port = os.getenv("PORT")
app.run(host="0.0.0.0", port=port)

