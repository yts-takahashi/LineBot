import time
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('6y2KhFNjNVHKX1DWO1pIhRD7kjXHAMMS8YIucPsDyfrFYsQtT/AA9iTkrMJ9JXFnP0l4bP2ksN3behUM3BHv9ysrMAUo4A2w7UsrKUo4ZlyqANJWxK6mc8HT+WoT8/QVX715Grc8RkAMqpAKKwk7fwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ec3315e8d0f214b8ab81435e2dc071ae')

start_times = {}


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "勉強開始":
        start_times[event.source.user_id] = time.time()
        return line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="計測を開始しました！"))
    if event.message.text == "勉強終了":
        elapsed_time = int(time.time() - start_times[event.source.user_id])
        del start_times[event.source.user_id]
        hour = elapsed_time // 3600
        minute = (elapsed_time % 3600) // 60
        second = elapsed_time % 60
        return line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"ただいまの勉強時間は{hour}時間{minute}分{second}秒です。お疲れ様でした！"))


if __name__ == "__main__":
    app.run()