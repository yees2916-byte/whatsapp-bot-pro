from flask import Flask, request
import google.generativeai as genai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد المفتاح من Render
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/bot", methods=['POST'])
def bot():
    user_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    
    # قائمة كلمات الترحيب للرد بالرسالة الخاصة
    greetings = ['سلام', 'مرحبا', 'أهلا', 'صباح الخير', 'مساء الخير', 'السلام عليكم']
    
    # إذا كانت الرسالة تحتوي على تحية
    if any(greet in user_msg for greet in greetings):
        welcome_text = (
            "مرحباً بك. أنا المساعد الذكي للأستاذ *عالم عبد الله*. \n\n"
            "أتشرف بخدمتك في رحاب هذا العمل الذي أهداه صاحبه صدقة جارية عن روح والده: "
            "*المجاهد حافظ القرآن الكريم، وإمام مسجد بلدية تيرسين بولاية سعيدة، الولي الصالح 'عالم الحاج المكي'* (رحمه الله وأسكنه فسيح جناته). \n\n"
            "💡 *للعلم:* أستقبل حالياً *20 رسالة يومياً* فقط. كيف يمكنني مساعدتك اليوم؟"
        )
        resp.message(welcome_text)
        return str(resp)

    try:
        # الموديل المعتمد (2.5-flash) مع حد 20 رسالة
        model = genai.GenerativeModel('gemini-2.5-flash')
        ai_response = model.generate_content(user_msg)
        resp.message(ai_response.text)
        
    except Exception as e:
        if "429" in str(e):
            resp.message("⚠️ عذراً، لقد انتهت حصة الـ 20 رسالة المجانية لهذا اليوم. نلتقي غداً بإذن الله!")
        else:
            resp.message(f"⚠️ عذراً، واجهت مشكلة تقنية بسيطة: {str(e)}")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
