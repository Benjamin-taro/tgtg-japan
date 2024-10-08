import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from datetime import datetime


app = Flask(__name__)


# LINE Messaging API のアクセストークンとシークレットを設定
line_bot_api = LineBotApi('8BPpPHpfULeAPom/gdDa22x3pMlkTjPKp9KtKB0dxVkZeMBbLoP6wlZaQYNLEkYqyBaucRJaIFS0qbfGx29ooebSaIgbQnUIyfZWhvJ6XvRAIOi65wcuRXNz0bHVdifLxayr/FCtYJoIpPl2INs0cwdB04t89/1O/w1cDnyilFU=')
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
# 時間帯に応じたクイックリプライを表示する
def get_quick_reply_buttons():
    now = datetime.now().hour  # 現在の時間を取得

    if 7 <= now < 17:  # 朝から夜の時間帯
        return QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="近隣のお店", text="近隣のお店")),
            QuickReplyButton(action=MessageAction(label="今日の夜ご飯を探す", text="今日の夜ご飯")),
            QuickReplyButton(action=MessageAction(label="今日のデザートを探す", text="今日のデザート")),
            QuickReplyButton(action=MessageAction(label="一覧の表示", text="一覧")),
        ])
    elif 17 <= now < 23:  # 夜の時間帯
        return QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="近隣のお店", text="近隣のお店")),
            QuickReplyButton(action=MessageAction(label="今日の夜ご飯を探す", text="今日の夜ご飯")),
            QuickReplyButton(action=MessageAction(label="今日のデザートを探す", text="今日のデザート")),
            QuickReplyButton(action=MessageAction(label="明日の朝ごはんを探す", text="明日の朝ご飯")),
            QuickReplyButton(action=MessageAction(label="一覧の表示", text="一覧")),
        ])
    else:  # 夜中
        return QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="近隣のお店", text="近隣のお店")),
            QuickReplyButton(action=MessageAction(label="明日の朝ごはんを探す", text="明日の朝ご飯")),
            QuickReplyButton(action=MessageAction(label="一覧の表示", text="一覧")),
        ])
    


# ユーザーからのメッセージに応じて返信を変える
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()  # ユーザーのメッセージを取得（小文字に変換して比較しやすくする）

    # 条件分岐による返信内容のカスタマイズ
    if '近隣のお店' in user_message:
        reply_text = "こちらが近隣のお店です。"
        #近隣のお店の情報を取得する処理を記述
    elif '今日の夜ご飯' in user_message:
        reply_text = "現在利用可能なお店はこちらです。"
        #今日の夜ご飯の情報を取得する処理を記述
    elif '今日のデザート' in user_message:
        reply_text = "現在利用可能なお店はこちらです。"
        #今日のデザートの情報を取得する処理を記述
    elif '明日の朝ご飯' in user_message:
        reply_text = "現在利用可能なお店はこちらです。"
        #明日の朝ご飯の情報を取得する処理を記述
    elif '一覧' in user_message:
        reply_text = "現在利用可能なお店はこちらです。"
        #一覧の情報を取得する処理を記述
    else:
        reply_text = "申し訳ありません、そのメッセージの意味は理解できませんが、他にお手伝いできることがあれば教えてください。"

    # ユーザーに返信とクイックリプライを送信
    quick_reply_buttons = get_quick_reply_buttons()  # 現在の時間に応じたクイックリプライボタンを取得
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text, quick_reply=quick_reply_buttons)
    )


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)