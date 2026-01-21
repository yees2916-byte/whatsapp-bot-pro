from flask import Flask, request
import google.generativeai as genai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد المفتاح
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# استخدام الموديل المتوافق "gemini-pro" ليعمل فوراً
model = genai.GenerativeModel('gemini-pro')

@app.route("/bot", methods=['POST'])
def bot():
    # تنظيف الرسالة
    user_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    
    # قائمة التحية
    greetings = ['سلام', 'مرحبا', 'مرحباً', 'أهلا', 'هلا', 'hi', 'hello', 'start', 'باسم الله']
    
    # 1. الرد على التحية (من الذاكرة)
    if any(greet in user_msg for greet in greetings):
        welcome_text = (
            "مرحباً بك. أنا المساعد الذكي للأستاذ *عالم عبد الله*. \n\n"
            "أتشرف بخدمتك في رحاب هذا العمل الذي أهداه صاحبه صدقة جارية عن روح والده: \n"
            "✨ *المجاهد حافظ القرآن الكريم، وإمام مسجد بلدية تيرسين بولاية سعيدة، الولي الصالح 'عالم الحاج المكي'* ✨\n"
            "(رحمه الله وأسكنه فسيح جناته). \n\n"
            "💡 تفضل بطرح سؤالك في أي مجال، وأنا في الخدمة."
        )
        resp.message(welcome_text)
        return str(resp)

    # 2. الرد على الأسئلة (باستخدام جوجل)
    try:
        ai_response = model.generate_content(user_msg)
        resp.message(ai_response.text)
        
    except Exception as e:
        # هذا الجزء هو الذي كان ناقصاً وتسبب في الخطأ
        resp.message("عذراً، حدث خطأ تقني بسيط.")
        print(f"Error: {e}")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
