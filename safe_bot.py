# coding: utf-8
import sys
import telebot
from telebot import types
import hashlib

TOKEN = sys.argv[1]
users = {}
markuphide = types.ReplyKeyboardHide()

class User:
    def __init__(self,chatid,text):
        #print ('Criado')
        self.id = chatid
        self.msg = '/start'
    def LastMessage(self,chatid,text):
        #print ('self.msg: '+text)
        self.msg = text
def listener(*messages):
    for m in messages:
        chatid = m.chat.id
        text = m.text
        user = None
        if users.has_key(chatid):
            user = users.get(chatid)
            if text == '/start':
                start = types.ReplyKeyboardMarkup()
                start.row('Hash','Password')
                tb.send_message(chatid,'Select one option',reply_markup=start)
            elif text == '/cancel':
                cancel = types.ReplyKeyboardMarkup()
                cancel.row('/start','/info')
                tb.send_message(chatid,'Done',reply_markup=cancel)
            elif text == '/info':
                info = ('This bot is under development!\n'
                'If you have any question or suggestion,\n'
                'please, talk to me!\nTwitter: grfgabriel\n'
                'Telegram: @GabrielRF\n'
                '\nCode available on GitHub:\n'
                'https://github.com/GabrielRF/Telegram-Safe-Bot')
                tb.send_message(chatid,info)
            elif text == 'Hash':
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
                password = types.ReplyKeyboardMarkup()
                password.row('Letters only','Numbers only')
                password.row('Letters and numbers')
                password.row('Letters, numbers and special characters')
                tb.send_message(chatid,'Choose the alfabet',reply_markup=password)
            else:
                start = types.ReplyKeyboardMarkup()
                start.row('Hash','Password')
                tb.send_message(chatid,'Select one option',reply_markup=start)
            print ('User: '+str(chatid)+' Text: '+text+' user.msg: '+user.msg)      #Debug only. Will be removed soon.
            user.LastMessage(user,text)
            #tb.send_message(chatid,'Send /start to reset')
        else:
            user = User(chatid,text)
            users[chatid] = user
            Start(chatid,text)
        #print(' ')

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


tb = telebot.TeleBot(TOKEN)
tb.set_update_listener(listener) #register listener
tb.polling()
while True:
    pass