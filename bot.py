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
        # قمنا بتثبيت الموديل على 1.5 flash لأنه الأكثر كرماً في النسخة المجانية
        model = genai.GenerativeModel('gemini-1.5-flash')
        ai_response = model.generate_content(user_msg)
        resp.message(ai_response.text)
    except Exception as e:
        # إذا انتهت الـ 1500 رسالة (وهذا صعب)، سيخبرك البوت
        if "429" in str(e):
            resp.message("⚠️ لقد استهلكت الكثير من الرسائل اليوم، حاول مجدداً بعد قليل.")
        else:
            resp.message(f"⚠️ عذراً، واجهت مشكلة تقنية: {str(e)}")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
