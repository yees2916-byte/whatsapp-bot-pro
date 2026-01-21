from flask import Flask
import google.generativeai as genai
import os

app = Flask(__name__)

# إعداد المفتاح
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# هذا الجزء سيعمل فور تشغيل السيرفر ويطبع الموديلات في الشاشة السوداء
print("----- بدأت عملية فحص الموديلات -----")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ موديل متاح: {m.name}")
except Exception as e:
    print(f"❌ خطأ في جلب الموديلات: {e}")
print("----- انتهى الفحص -----")

@app.route("/bot", methods=['POST'])
def bot():
    return "Bot is running check logs"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
