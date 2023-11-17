# main.py

from src.tarot_bot import TarotBot
from src.gpt_assistant import GPTAssistant
from src.database import DataBase
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
