from flask import Flask, request
import google.generativeai as genai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد جوجل
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def get_response(user_input):
    # قائمة بأسماء الموديلات الممكنة - سيجربها البوت واحداً تلو الآخر
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(user_input)
            return response.text
        except Exception:
            continue # إذا فشل موديل ينتقل للذي يليه
    return "عذراً، لم أستطع العثور على موديل نشط في حسابك حالياً."

@app.route("/bot", methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    if not incoming_msg:
        msg.body('أنا أسمعك، تفضل بسؤالك.')
        return str(resp)

    # تشغيل البحث التلقائي عن الموديل
    reply = get_response(incoming_msg)
    msg.body(reply)
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
