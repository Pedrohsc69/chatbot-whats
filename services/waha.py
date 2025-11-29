import os
import requests


class Waha:

    def __init__(self):
        self.__api_url = 'http://waha:3000'

        self.__api_key = os.getenv("WAHA_API_KEY")
        self.__headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.__api_key
        }

    def send_message(self, chat_id, message):
        url = f'{self.__api_url}/api/sendText'

        # headers = {
        #     'Content-Type': 'application/json',
        # }

        payload = {
            'session': 'default',
            'chatId': chat_id,
            'text': message,
        }

        print(f"[WAHA] Enviando mensagem para {url}")
        print("[WAHA] Payload:", payload)

        # requests.post(
        #     url=url,
        #     json=payload,
        #     headers=headers,
        # )

        response = requests.post(url=url, json=payload, headers=self.__headers)

        print("[WAHA] Status:", response.status_code)
        # print("[WAHA] Resposta:", response.text)

    def start_typing(self, chat_id):
        url = f'{self.__api_url}/api/startTyping'

        # headers = {
        #     'Content-Type': 'application/json',
        # }

        payload = {
            'session': 'default',
            'chatId': chat_id,
        }

        print(f"[WAHA] startTyping -> {url}")
        print("[WAHA] Payload:", payload)

        # requests.post(
        #     url=url,
        #     json=payload,
        #     headers=headers,
        # )

        response = requests.post(url=url, json=payload, headers=self.__headers)
        print("[WAHA] Resposta typing:", response.status_code, response.text)


    def stop_typing(self, chat_id):
        url = f'{self.__api_url}/api/stopTyping'

        # headers = {
        #     'Content-Type': 'application/json',
        # }

        payload = {
            'session': 'default',
            'chatId': chat_id,
        }

        print(f"[WAHA] stopTyping -> {url}")
        print("[WAHA] Payload:", payload)

        # requests.post(
        #     url=url,
        #     json=payload,
        #     headers=headers,
        # )

        response = requests.post(url=url, json=payload, headers=self.__headers)
        print("[WAHA] Resposta stopTyping:", response.status_code, response.text)
