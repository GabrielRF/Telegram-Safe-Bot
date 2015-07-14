# coding: utf-8
import sys
import telebot
from telebot import types
import hashlib
import string
import random
import time

from parse_rest.connection import register
from parse_rest.datatypes import Object
from parse_rest.user import User

TOKEN = sys.argv[1]
PARSE_APP_KEY = sys.argv[2]
PARSE_REST_API_KEY = sys.argv[3]

users = {}
markuphide = types.ReplyKeyboardHide()

class Usage(Object):
    pass

def update_analytics(m_chat_id, m_group):
    set_group = 'user.' + str(m_group) + ' = 1'
    obj_id = Usage.Query.filter(user_id=int(m_chat_id)).limit(1)
    if len(str(obj_id)) < 4:
        user = Usage()
        user.user_id = int(m_chat_id)
        exec(set_group)
        user.save()
    else:
        try:
            uid = str(obj_id)[8:-2]
            user = Usage.Query.get(objectId=uid)
            user.increment(str(m_group))
            user.save()
        except Exception:
            pass

class User:
    def __init__(self,chatid,text):
        self.id = chatid
        self.msg = '/start'
    def LastMessage(self,chatid,text):
        #print ('self.msg: '+text)
        self.msg = text
        
def listener(messages):
    for m in messages:
        chatid = m.chat.id
        user = None
        if m.content_type == 'text':
            text = m.text
            text = text.encode('utf-8')
        if users.has_key(chatid) and m.content_type == 'text':
            user = users.get(chatid)
            if text == '/start':
                update_analytics(chatid, 'Start')
                start = types.ReplyKeyboardMarkup()
                start.row('Hash','Password')
                tb.send_message(chatid,'Select one option',reply_markup=start)
            elif text == '/cancel':
                update_analytics(chatid, 'Cancel')
                cancel = types.ReplyKeyboardMarkup()
                cancel.row('/start','/info')
                tb.send_message(chatid,'Done',reply_markup=cancel)
            elif text == '/info':
                update_analytics(chatid, 'Info')
                info = ('This bot is under constant development!\n'
                'If you have any question or suggestion,\n'
                'please, talk to me!\nTwitter: grfgabriel\n'
                'Telegram: @GabrielRF\n'
                '\nCode available on GitHub:\n'
                'https://github.com/GabrielRF/Telegram-Safe-Bot\n'
                '\nRate the bot:\nhttps://telegram.me/storebot?start=safe_bot')
                tb.send_message(chatid,info)
            elif text == 'Hash':
                update_analytics(chatid, 'Hash')
                hash = types.ReplyKeyboardMarkup()
                hash.row('MD5','SHA1','SHA224')
                hash.row('SHA256','SHA384','SHA512')
                tb.send_message(chatid,'Choose one Hash algorithm',reply_markup=hash)
            elif (text == 'MD5' or text == 'SHA1' or text == 'SHA224' or text == 'SHA256' or text == 'SHA384' or text == 'SHA512'):
                tb.send_message(chatid,'Now send the message',reply_markup=markuphide)
                text = 'HASH '+text
            elif user.msg == 'HASH MD5': tb.send_message(chatid,MD5(chatid,text))
            elif user.msg == 'HASH SHA1':tb.send_message(chatid,SHA1(chatid,text))
            elif user.msg == 'HASH SHA224':tb.send_message(chatid,SHA224(chatid,text))
            elif user.msg == 'HASH SHA256':tb.send_message(chatid,SHA256(chatid,text))
            elif user.msg == 'HASH SHA384':tb.send_message(chatid,SHA384(chatid,text))
            elif user.msg == 'HASH SHA512':tb.send_message(chatid,SHA512(chatid,text))
            elif text == 'Password':
                update_analytics(chatid, 'Password')
                password = types.ReplyKeyboardMarkup()
                password.row('Letters only','Numbers only')
                password.row('Letters and numbers')
                password.row('Letters, numbers and special characters')
                tb.send_message(chatid,'Choose the alfabet',reply_markup=password)
            elif text == 'Letters only' or text == 'Numbers only' or text == 'Letters and numbers' or text == 'Letters, numbers and special characters':
                tb.send_message(chatid,'Now send me the length (up to 100)',reply_markup=markuphide)
            elif user.msg == 'Letters only': tb.send_message(chatid,PassGen(text,string.ascii_uppercase+string.ascii_lowercase))
            elif user.msg == 'Numbers only': tb.send_message(chatid,PassGen(text,string.digits))
            elif user.msg == 'Letters and numbers': tb.send_message(chatid,PassGen(text,string.ascii_uppercase+string.ascii_lowercase+string.digits))
            elif user.msg == 'Letters, numbers and special characters': tb.send_message(chatid,PassGen(text,string.ascii_uppercase+string.ascii_lowercase+string.digits+string.punctuation))
            else:
                start = types.ReplyKeyboardMarkup()
                start.row('Hash','Password')
                tb.send_message(chatid,'Select one option',reply_markup=start)
            #print ('User: '+str(chatid)+' Text: '+text+' user.msg: '+user.msg)      #Debug only. 
            user.LastMessage(user,text)
        elif m.content_type != 'text': tb.send_message(chatid,'Please, send me only text.')
        else:
            update_analytics(chatid, 'Text')
            user = User(chatid,text)
            users[chatid] = user
            Start(chatid,text)
            
def Start(chatid,text):
    start = types.ReplyKeyboardMarkup()
    start.row('Hash','Password')
    tb.send_message(chatid,'Welcome!\nSelect one option',reply_markup=start)
def Hash(chatid,text):
    tb.send_message(chatid,text)
def MD5(chatid,text):    return hashlib.md5(text).hexdigest()
def SHA1(chatid,text):   return hashlib.sha1(text).hexdigest()
def SHA224(chatid,text): return hashlib.sha224(text).hexdigest()
def SHA256(chatid,text): return hashlib.sha256(text).hexdigest()
def SHA384(chatid,text): return hashlib.sha384(text).hexdigest()
def SHA512(chatid,text): return hashlib.sha512(text).hexdigest()
def PassGen(size,chars):
    try:
        size=int(size)
        if size > 100: size = 100
        elif size < 0: size = size*(-1)
        elif size == 0: size = 8
        return ''.join(random.choice(chars) for _ in range(size))
    except:
        return 'I was expecting an integer.'

register(PARSE_APP_KEY,PARSE_REST_API_KEY)
tb = telebot.TeleBot(TOKEN)
tb.set_update_listener(listener)
tb.polling()
while True:
    time.sleep(20)