# main.py
import os
from configparser import ConfigParser
from src.database.database_factory import get_database
from src.gpt_assistant import GPTAssistant
from src.tarot_bot import TarotBot


def load_config(environment):
    cfg = ConfigParser()

    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs', 'config.ini')
    cfg.read(config_path)

    return cfg[environment]


if __name__ == '__main__':
    config = load_config("prod")

    token = config.get('tgkey_token')
    api_key = config.get('gptkey_api_key')

    db_url = f"postgresql://{config.get('user')}:{config.get('password')}@{config.get('host')}/{config.get('db_name')}"
    database = get_database(db_type=config.get('db_type'), db_url=db_url)

    gpt_assistant = GPTAssistant(api_key)
    tarot_bot = TarotBot(token, database, gpt_assistant)

    tarot_bot.main()
