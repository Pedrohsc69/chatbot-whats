from flask import Flask, request, jsonify
from bot.ai_bot import AIBot
from services.waha import Waha

app = Flask(__name__)
user_language = {}

# -----------------------------
#  UTILITÁRIOS DE MENSAGENS
# -----------------------------

def send_initial_language_question(waha, chat_id):
    msg = (
        "Olá! Para qual idioma você deseja que eu traduza suas mensagens?\n\n"
        "Exemplos:\n- Inglês\n- Espanhol\n- Francês\n- Alemão\n- Japonês\n- Italiano\n\n"
        "Digite apenas o nome do idioma.\n\n"
        "📌 *Comandos disponíveis:*\n"
        "*/idioma* - mudar o idioma\n"
        "*/parar* - parar as traduções\n"
        "*/voltar* - voltar a traduzir"
    )
    waha.send_message(chat_id, msg)


def send_language_set_message(waha, chat_id, idioma):
    waha.send_message(chat_id, f"Perfeito! Agora todas as suas mensagens serão traduzidas para *{idioma}*.")


def send_language_change_request(waha, chat_id):
    waha.send_message(
        chat_id,
        "Claro! Para qual idioma deseja alterar a tradução?\n\n"
        "Exemplos:\nInglês, Espanhol, Japonês, Francês..."
    )


def send_translation_off_message(waha, chat_id):
    waha.send_message(
        chat_id,
        "👌 Tradução desativada!\n\nSe quiser ativar novamente, envie:\n/voltar"
    )


def send_translation_on_message(waha, chat_id):
    waha.send_message(chat_id, "Ótimo! Para qual idioma deseja ativar a tradução novamente?")


# -----------------------------
#  LÓGICA DE COMANDOS
# -----------------------------

def handle_commands(waha, chat_id, message):
    if message.startswith("/idioma"):
        user_language[chat_id] = None
        send_language_change_request(waha, chat_id)
        return True

    if message.startswith("/parar"):
        user_language[chat_id] = "off"
        send_translation_off_message(waha, chat_id)
        return True

    if message.startswith("/voltar"):
        user_language[chat_id] = None
        send_translation_on_message(waha, chat_id)
        return True

    return False


# -----------------------------
#  LÓGICA PRINCIPAL DO BOT
# -----------------------------

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json

    waha = Waha()
    ai_bot = AIBot()

    chat_id = data['payload']['from']
    message = data['payload']['body'].strip().lower()

    
    if chat_id.endswith("@g.us"):
        print('Grupo ignorado')
        return jsonify({'status': 'ignored - group'}), 200

    
    if chat_id not in user_language:
        user_language[chat_id] = None
        send_initial_language_question(waha, chat_id)
        return jsonify({'status': 'ask_language'}), 200

    
    if user_language[chat_id] is None:
        user_language[chat_id] = message.capitalize()
        send_language_set_message(waha, chat_id, user_language[chat_id])
        return jsonify({'status': 'language_set'}), 200

    
    if handle_commands(waha, chat_id, message):
        return jsonify({'status': 'command_executed'}), 200

    
    if user_language[chat_id] == "off":
        waha.send_message(chat_id, message)
        return jsonify({'status': 'translation_off_pass'}), 200

    
    idioma = user_language[chat_id]

    waha.start_typing(chat_id)
    response = ai_bot.invoke(texto=message, idioma=idioma)
    waha.send_message(chat_id, response)
    waha.stop_typing(chat_id)

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
