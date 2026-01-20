from flask import Flask, request
import google.generativeai as genai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد المفتاح
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def select_working_model():
    """وظيفة ذكية تبحث عن الموديل المتاح في حسابك لتجنب خطأ 404"""
    try:
        # نسأل جوجل عن الموديلات التي تدعم إنشاء المحتوى
        available_models = [m.name for m in genai.list_models() 
                           if 'generateContent' in m.supported_generation_methods]
        
        # قائمة الأولويات (نبحث عن الأكثر كرماً والأحدث)
        # نضع 1.5-flash أولاً لأنه يعطي 1500 رسالة يومياً
        priorities = ['models/gemini-1.5-flash', 'models/gemini-1.5-flash-latest', 'models/gemini-1.0-pro']
        
        for p in priorities:
            if p in available_models:
                return p
        
        # إذا لم يجد أياً من المذكور، يأخذ أول موديل متاح في القائمة
        return available_models[0] if available_models else 'models/gemini-1.5-flash'
    except Exception as e:
        print(f"Error listing models: {e}")
        return 'models/gemini-1.5-flash'

# البوت يختار الموديل عند التشغيل
CHOSEN_MODEL = select_working_model()
model = genai.GenerativeModel(CHOSEN_MODEL)

@app.route("/bot", methods=['POST'])
def bot():
    user_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    
    try:
        # استخدام الموديل المختار تلقائياً
        ai_response = model.generate_content(user_msg)
        resp.message(ai_response.text)
    except Exception as e:
        # إذا حدث خطأ الكوتا (429) أو غيره، يخبرنا باسم الموديل المستخدم
        resp.message(f"⚠️ الموديل: {CHOSEN_MODEL}\nالخطأ: {str(e)}")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
