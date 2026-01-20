from flask import Flask, request
import google.generativeai as genai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد المفتاح
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/bot", methods=['POST'])
def bot():
    user_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()

    try:
        # استخدام أحدث مسمى للموديل لضمان العمل
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        ai_response = model.generate_content(user_msg)
        resp.message(ai_response.text)
    except Exception as e:
        # في حال وجود مشكلة تقنية بسيطة
        resp.message(f"⚠️ عذراً، حدث خطأ في معالجة الرد: {str(e)}")

    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
