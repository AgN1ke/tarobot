# main.py

from telega import TarotBot
from gpt import GPTAssistant
from bd import DataBase
import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('promt.ini')
    token = config.get('tgkey', 'token')
    api_key = config.get('gptkey', 'api_key')

    db = DataBase()
    gpt_assistant = GPTAssistant(api_key)
    tarot_bot = TarotBot(token, db, gpt_assistant)
    tarot_bot.main()
