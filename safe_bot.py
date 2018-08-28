import configparser
import hashlib
import random
import string
import telebot
from telebot import types

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.sections()
    BOT_CONFIG_FILE = '/usr/local/bin/Telegram-Safe-Bot/bot.conf'
    config.read(BOT_CONFIG_FILE)

    try:
        TOKEN = config['SAFEBOT']['TOKEN']
        start_txt = config['SAFEBOT']['START']
        password_txt = config['SAFEBOT']['PASSWORD']
        hash_txt = config['SAFEBOT']['HASH']
        text_txt = config['SAFEBOT']['TEXT']
        size_txt = config['SAFEBOT']['SIZE']
        info_txt = config['SAFEBOT']['INFO']
    except:
        TOKEN = 'test'
        pass

    bot = telebot.TeleBot(TOKEN)

    menu_start = types.InlineKeyboardMarkup()
    btn_password = types.InlineKeyboardButton('Password', callback_data='password')
    btn_hash = types.InlineKeyboardButton('Hash', callback_data='hash')
    menu_start.row(btn_password, btn_hash)

    menu_hash = types.InlineKeyboardMarkup()
    btn_hash_md5 = types.InlineKeyboardButton('MD5', callback_data='md5')
    btn_hash_sha1 = types.InlineKeyboardButton('SHA1', callback_data='sha1')
    btn_hash_sha224 = types.InlineKeyboardButton('SHA224', callback_data='sha224')
    btn_hash_sha256 = types.InlineKeyboardButton('SHA256', callback_data='sha256')
    btn_hash_sha384 = types.InlineKeyboardButton('SHA384', callback_data='sha384')
    btn_hash_sha512 = types.InlineKeyboardButton('SHA512', callback_data='sha512')
    menu_hash.row(btn_hash_md5, btn_hash_sha1, btn_hash_sha224)
    menu_hash.row(btn_hash_sha256, btn_hash_sha384, btn_hash_sha512)

    menu_pwd = types.InlineKeyboardMarkup()
    btn_pwd_let = types.InlineKeyboardButton('Letters only', callback_data='let')
    btn_pwd_num = types.InlineKeyboardButton('Numbers only', callback_data='num')
    btn_pwd_l_n = types.InlineKeyboardButton('Letters and numbers', callback_data='l_n')
    btn_pwd_lnc = types.InlineKeyboardButton('Letter, numbers and characters', callback_data='lnc')
    menu_pwd.row(btn_pwd_let, btn_pwd_num)
    menu_pwd.row(btn_pwd_l_n)
    menu_pwd.row(btn_pwd_lnc)

    def PassGen(size, chars):
        try:
            size=int(size)
            if size > 100: size = 100
            elif size < 0: size = size*(-1)
            elif size == 0: size = 8
            return ''.join(random.choice(chars) for _ in range(size))
        except:
            return 'I was expecting an integer.'

    def pwd_let(message):
        digest = PassGen(message.text, string.ascii_uppercase+string.ascii_lowercase)
        bot.send_message(message.from_user.id, digest)

    def pwd_num(message):
        digest = PassGen(message.text, string.digits)
        bot.send_message(message.from_user.id, digest)

    def pwd_l_n(message):
        digest = PassGen(message.text, string.ascii_uppercase+string.ascii_lowercase+string.digits)
        bot.send_message(message.from_user.id, digest)

    def pwd_lnc(message):
        digest = PassGen(message.text, string.ascii_uppercase+string.ascii_lowercase+string.digits+string.punctuation)
        bot.send_message(message.from_user.id, digest)

    def hash_md5(message):
        digest = hashlib.md5(message.text.encode('utf-8')).hexdigest()
        bot.send_message(message.from_user.id, digest)

    def hash_sha1(message):
        digest = hashlib.sha1(message.text.encode('utf-8')).hexdigest()
        bot.send_message(message.from_user.id, digest)

    def hash_sha224(message):
        digest = hashlib.sha224(message.text.encode('utf-8')).hexdigest()
        bot.send_message(message.from_user.id, digest)

    def hash_sha256(message):
        digest = hashlib.sha256(message.text.encode('utf-8')).hexdigest()
        bot.send_message(message.from_user.id, digest)

    def hash_sha384(message):
        digest = hashlib.sha384(message.text.encode('utf-8')).hexdigest()
        bot.send_message(message.from_user.id, digest)

    def hash_sha512(message):
        digest = hashlib.sha512(message.text.encode('utf-8')).hexdigest()
        bot.send_message(message.from_user.id, digest)

    @bot.message_handler(commands=['info'])
    def start(message):
        bot.send_chat_action(message.chat.id, 'typing')
        msg = bot.send_message(message.from_user.id, info_txt,
            parse_mode='HTML', disable_web_page_preview=True)

    @bot.message_handler(commands=['start','cancel'])
    def start(message):
        bot.send_chat_action(message.chat.id, 'typing')
        msg = bot.send_message(message.from_user.id, start_txt, 
            parse_mode='HTML', reply_markup=menu_start)

    @bot.callback_query_handler(lambda q: q.data == 'password')
    def password(message):
        bot.answer_callback_query(message.id)
        msg = bot.send_message(message.from_user.id, password_txt, 
            parse_mode='HTML', reply_markup=menu_pwd)

    @bot.callback_query_handler(lambda q: q.data == 'hash')
    def hash(message):
        bot.answer_callback_query(message.id)
        msg = bot.send_message(message.from_user.id, hash_txt, 
            parse_mode='HTML', reply_markup=menu_hash)

    @bot.callback_query_handler(lambda q: q.data == 'md5')
    def md5(message):
        bot.answer_callback_query(message.id)
        msg = bot.send_message(message.from_user.id, text_txt,
            parse_mode='HTML')
        bot.register_next_step_handler(msg, hash_md5)

    @bot.callback_query_handler(lambda q: q.data == 'sha1')
    def sha1(message):
        bot.answer_callback_query(message.id)
        msg = bot.send_message(message.from_user.id, text_txt,
            parse_mode='HTML')
        bot.register_next_step_handler(msg, hash_sha1)

    @bot.callback_query_handler(lambda q: q.data == 'sha224')
    def sha224(message):
        bot.answer_callback_query(message.id)
        msg = bot.send_message(message.from_user.id, text_txt,
            parse_mode='HTML')
        bot.register_next_step_handler(msg, hash_sha224)

    @bot.callback_query_handler(lambda q: q.data == 'sha256')
    def sha256(message):
        bot.answer_callback_query(message.id)
        msg = bot.send_message(message.from_user.id, text_txt,
            parse_mode='HTML')
        bot.register_next_step_handler(msg, hash_sha256)

    @bot.callback_query_handler(lambda q: q.data == 'sha384')
    def sha384(message):
        bot.answer_callback_query(message.id)
        msg = bot.send_message(message.from_user.id, text_txt,
            parse_mode='HTML')
        bot.register_next_step_handler(msg, hash_sha384)

    @bot.callback_query_handler(lambda q: q.data == 'sha512')
    def sha512(message):
        bot.answer_callback_query(message.id)
        msg = bot.send_message(message.from_user.id, text_txt,
            parse_mode='HTML')
        bot.register_next_step_handler(msg, hash_sha512)

    @bot.callback_query_handler(lambda q: q.data == 'let')
    def let(message):
        bot.answer_callback_query(message.id)
        msg = bot.send_message(message.from_user.id, size_txt,
            parse_mode='HTML')
        bot.register_next_step_handler(msg, pwd_let)

    @bot.callback_query_handler(lambda q: q.data == 'num')
    def num(message):
        bot.answer_callback_query(message.id)
        msg = bot.send_message(message.from_user.id, size_txt,
            parse_mode='HTML')
        bot.register_next_step_handler(msg, pwd_num)

    @bot.callback_query_handler(lambda q: q.data == 'l_n')
    def l_n(message):
        bot.answer_callback_query(message.id)
        msg = bot.send_message(message.from_user.id, size_txt,
            parse_mode='HTML')
        bot.register_next_step_handler(msg, pwd_l_n)

    @bot.callback_query_handler(lambda q: q.data == 'lnc')
    def lnc(message):
        bot.answer_callback_query(message.id)
        msg = bot.send_message(message.from_user.id, size_txt,
            parse_mode='HTML')
        bot.register_next_step_handler(msg, pwd_lnc)

    if TOKEN != 'test':
        bot.polling(none_stop=True)

