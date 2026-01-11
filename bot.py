from flask import Flask, request
import google.generativeai as genai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد المفتاح
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/bot", methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    try:
        # استخدام الاسم المحدث للموديل (gemini-1.5-flash-latest)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(incoming_msg)
        msg.body(response.text)
    except Exception as e:
        # إذا فشل، نحاول استخدام النسخة 1.0 (الأكثر استقراراً)
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(incoming_msg)
            msg.body(response.text)
        except Exception as e2:
            msg.body(f"⚠️ تنبيه: جوجل تطلب تحديث الربط. الخطأ: {str(e2)}")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
