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
        # الاسم الجديد والمستقر لموديل جوجل (بدون كلمة models/ وبدون v1beta)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(incoming_msg)
        msg.body(response.text)
    except Exception as e:
        # إذا فشل، سنقوم بجلب الأسماء المتاحة فعلياً في حسابك الآن
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            models_list = "\n".join(available_models)
            msg.body(f"⚠️ الموديل الافتراضي لم يعمل.\nالأسماء المتاحة في حسابك هي:\n{models_list}")
        except Exception as e2:
            msg.body(f"⚠️ خطأ في الصلاحيات: تأكد أن المفتاح API Key مفعّل ومربوط بمشروع جديد.")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
