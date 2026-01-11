from flask import Flask, request
import google.generativeai as genai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def get_working_model():
    try:
        # البحث التلقائي عن الموديلات المتاحة في حسابك
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_working_model()

@app.route("/bot", methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()
    try:
        response = model.generate_content(incoming_msg)
        msg.body(response.text)
    except Exception as e:
        msg.body("أهلاً! أنا أعمل الآن، اطلب مني أي شيء.")
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
