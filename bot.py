from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os

app = Flask(__name__)

# جلب المفتاح من إعدادات السيرفر (للأمان)
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

# صفحة فحص الحالة (للتأكد أن السيرفر يعمل)
@app.route('/', methods=['GET'])
def home():
    return "✅ Server is Running! WhatsApp Bot is ready."

@app.route("/bot", methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    print(f"User sent: {incoming_msg}")
    
    resp = MessagingResponse()
    msg = resp.message()

    if not client:
        msg.body("Error: API Key is missing on the server.")
        return str(resp)

    try:
        # إرسال الرسالة للذكاء الاصطناعي
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant on WhatsApp."},
                {"role": "user", "content": incoming_msg}
            ],
            max_tokens=300
        )
        reply_text = response.choices[0].message.content
        msg.body(reply_text)
    except Exception as e:
        print(f"Error: {e}")
        msg.body("عذراً، حدث خطأ مؤقت في السيرفر.")

    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
