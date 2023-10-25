# -*- coding: utf-8 -*-

import openai
import configparser


class GPTAssistant:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.chat_histories = {}

    def gpt_request(self, chat_id, prompt, max_tokens):
        config = configparser.ConfigParser()
        config.read('promt.ini')
        zagovor = config.get('zagovor', 'text')

        print(f"Запрос к GPT: {prompt}")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": zagovor},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )

            bot_response = response['choices'][0]['message']['content']
            self.chat_histories.setdefault(chat_id, [])
            self.chat_histories[chat_id].append({"role": "assistant", "content": bot_response})
            print(f"Bot: {bot_response}")

            return bot_response

        except Exception as e:
            print(f"Произошла ошибка при запросе к OpenAI: {e}")
