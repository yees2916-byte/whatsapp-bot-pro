
from flask import Flask, request
import google.generativeai as genai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد مفتاح جوجل جميني
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

@app.route("/bot", methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    if not incoming_msg:
        msg.body('أنا هنا! أرسل لي أي سؤال.')
        return str(resp)

    try:
        # إرسال السؤال إلى جوجل
        response = model.generate_content(incoming_msg)
        bot_reply = response.text
        msg.body(bot_reply)
    except Exception as e:
        msg.body('عذراً، حدث خطأ بسيط. حاول مرة أخرى لاحقاً.')
        print(f"Error: {e}")

    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
