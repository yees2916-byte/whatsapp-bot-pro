from flask import Flask, request
import google.generativeai as genai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد المفتاح
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def find_best_model():
    """هذه الوظيفة 'تسأل' جوجل عن الموديلات المتاحة وتختار الأنسب"""
    try:
        # طلب قائمة الموديلات المتاحة لهذا المفتاح
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # ترتيب الأولويات (نبحث عن الأحدث أولاً)
        priorities = ['models/gemini-2.5-flash', 'models/gemini-1.5-flash', 'models/gemini-pro']
        
        for p in priorities:
            if p in models:
                return p
        
        # إذا لم يجد أياً منها، يختار أول موديل متاح في القائمة
        return models[0] if models else 'models/gemini-1.5-flash'
    except Exception as e:
        print(f"خطأ في البحث عن الموديل: {e}")
        return 'models/gemini-1.5-flash' # حل احتياطي

# البوت 'يسأل' عند التشغيل ويحدد الموديل
SELECTED_MODEL = find_best_model()
model = genai.GenerativeModel(SELECTED_MODEL)

@app.route("/bot", methods=['POST'])
def bot():
    user_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    
    try:
        # استخدام الموديل الذي تم اختياره بعد 'السؤال'
        ai_response = model.generate_content(user_msg)
        resp.message(ai_response.text)
    except Exception as e:
        # في حال حدوث خطأ، يرسل لنا البوت تفاصيل الموديل الذي حاول استخدامه
        resp.message(f"⚠️ الموديل المستخدم: {SELECTED_MODEL}\nالخطأ: {str(e)}")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
