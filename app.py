import time
import random

from dotenv import load_dotenv
load_dotenv()


from flask import Flask, request, jsonify

from services.waha import Waha


app = Flask(__name__)


@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json

    print(f'EVENTO RECEBIDO: {data}')

    waha = Waha()

    try:
        chat_id = data['payload']['from']
        print(f"[WEBHOOK] chat_id extraído: {chat_id}")
    except Exception as e:
        print("[ERRO] Falha ao extrair chat_id:", e)
        return jsonify({'error': 'invalid payload'}), 400
    
    
    print("[WEBHOOK] Chamando start_typing()...")
    waha.start_typing(chat_id=chat_id)

    time.sleep(random.randint(3, 10))

    print("[WEBHOOK] Chamando send_message()...")
    waha.send_message(
        chat_id=chat_id,
        message='Resposta Automática :)',
    )

    print("[WEBHOOK] Chamando stop_typing()...")
    waha.stop_typing(chat_id=chat_id)

    print("[WEBHOOK] Finalizado com sucesso.")
    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
