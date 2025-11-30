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

        payload = {
            'session': 'default',
            'chatId': chat_id,
            'text': message,
        }

        requests.post(url=url, json=payload, headers=self.__headers)

    def start_typing(self, chat_id):
        url = f'{self.__api_url}/api/startTyping'

        payload = {
            'session': 'default',
            'chatId': chat_id,
        }

        requests.post(url=url, json=payload, headers=self.__headers)


    def stop_typing(self, chat_id):
        url = f'{self.__api_url}/api/stopTyping'


        payload = {
            'session': 'default',
            'chatId': chat_id,
        }

        requests.post(url=url, json=payload, headers=self.__headers)