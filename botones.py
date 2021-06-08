from telebot import types
import config

botones = {}
    
def getBoton(buttonId):
    return types.InlineKeyboardButton(config.mensajes[buttonId],callback_data=buttonId)

def getTeclado(*botonesId):
    markup  = types.InlineKeyboardMarkup()
    for botonId in botonesId:
        markup.add(getBoton(botonId))
    return markup
