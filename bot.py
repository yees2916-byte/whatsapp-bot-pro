from flask import Flask, request
import google.generativeai as genai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد جوجل
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# استخدام موديل 1.5-pro لضمان أعلى توافق
model = genai.GenerativeModel('gemini-1.5-pro')

@app.route("/bot", methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    if not incoming_msg:
        msg.body('أهلاً بك! أنا أعمل الآن. أرسل لي أي سؤال.')
        return str(resp)

    try:
        # محاولة توليد رد
        response = model.generate_content(incoming_msg)
        msg.body(response.text)
    except Exception as e:
        # في حال حدوث خطأ، سيصلك وصف الخطأ في الواتساب مباشرة
        msg.body(f"⚠️ تنبيه من النظام: {str(e)}")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
