import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

app = Flask(__name__)

# إعداد مفتاح Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# تحديد الموديل (تم تعديل الاسم ليتوافق مع الحل الجديد)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# هذا الجزء سيعمل فور تشغيل السيرفر ويطبع الموديلات في الشاشة السوداء (للتأكد فقط)
print("----- بدأت عملية فحص الموديلات -----")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ موديل متاح: {m.name}")
except Exception as e:
    print(f"❌ خطأ في جلب الموديلات: {e}")
print("----- انتهى الفحص -----")

@app.route("/bot", methods=["POST"])
def bot():
    # استقبال النص القادم من Twilio
    incoming_msg = request.values.get("Body", "").strip()

    # إنشاء المتغير للاستخدام أدناه
    reply_text =
