import telebot
from environs import Env
import sys
run_path = sys.path[0]
env = Env()
env.read_env(f'{run_path}/.env')  # read .env file, if it exists
TEL_TOKEN = env('TEL_TOKEN')
CHAT_ID = env('CHAT_ID')
bot = telebot.TeleBot(
    TEL_TOKEN, parse_mode=None
)
