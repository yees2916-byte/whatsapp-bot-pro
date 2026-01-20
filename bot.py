from flask import Flask, request
import google.generativeai as genai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد المفتاح الجديد من Render
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/bot", methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    try:
        # استخدام الموديل الأحدث الذي يدعم كل المفاتيح الجديدة
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(incoming_msg)
        msg.body(response.text)
    except Exception as e:
        msg.body(f"⚠️ البوت متصل بالمفتاح الجديد، لكن هناك ملاحظة: {str(e)}")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
