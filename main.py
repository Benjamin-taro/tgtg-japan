import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


app = Flask(__name__)


# LINE Messaging API のアクセストークンとシークレットを設定
line_bot_api = LineBotApi('1654881603')
handler = WebhookHandler('b3c1ec9d12b3d7e8916792bca9aeff28')

@app.route("/callback", methods=['POST'])
def callback():
    # Webhookからのリクエストを受け取る
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# ユーザーからのメッセージに応じて返信を変える
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()  # ユーザーのメッセージを取得（小文字に変換して比較しやすくする）

    # 条件分岐による返信内容のカスタマイズ
    if 'こんにちは' in user_message:
        reply_text = "こんにちは！何かお手伝いできることはありますか？"
    elif 'ありがとう' in user_message:
        reply_text = "どういたしまして！お役に立てて嬉しいです。"
    elif '天気' in user_message:
        reply_text = "天気については、今のところわかりませんが、ニュースアプリで確認してみてください。"
    else:
        reply_text = "申し訳ありません、そのメッセージの意味は理解できませんが、他にお手伝いできることがあれば教えてください。"

    # ユーザーに返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)