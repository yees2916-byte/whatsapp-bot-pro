from flask import Flask, request
import google.generativeai as genai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/bot", methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    try:
        # 1. جلب قائمة كل الموديلات المتاحة لك فعلياً
        available_models = [m.name for m in genai.list_models()]
        
        # 2. محاولة استخدام الموديل الأكثر استقراراً (بدون كلمة beta)
        # سنجرب gemini-1.5-flash أو gemini-pro
        model_to_use = 'gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else 'gemini-pro'
        
        model = genai.GenerativeModel(model_to_use)
        response = model.generate_content(incoming_msg)
        msg.body(response.text)
        
    except Exception as e:
        # إذا فشل، سيرسل لك القائمة التي وجدها لتخبرني بها
        models_str = ", ".join([m.name for m in genai.list_models()])
        msg.body(f"⚠️ لم أجد الموديل. الموديلات المتاحة في حسابك هي:\n{models_str}\n\nالخطأ: {str(e)}")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
