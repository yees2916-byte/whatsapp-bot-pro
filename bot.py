from flask import Flask, request
import google.generativeai as genai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد المفتاح
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

@app.route("/bot", methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    try:
        # محاولة استخدام موديل Flash المجاني
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(incoming_msg)
        msg.body(response.text)
    except Exception as e:
        # هذه المرة، البوت سيرسل لك "نص الخطأ" لتعرف المشكلة
        msg.body(f"⚠️ خطأ تقني: {str(e)}")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
