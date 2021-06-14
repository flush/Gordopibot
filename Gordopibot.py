from telebot import types

import config
import botones
import flujoAltaUsuario
import flujoApertura
import flujoComun
import flujoPartida
from gruposHelper import *

#Start handler

@config.bot.message_handler(commands=['jugar'])
def jugar(message):

    usuario = config.usuarioDB.getUsuario(message.from_user.id);
    if not usuario and not grupoAutorizado(message.chat.id):
        markup  = types.InlineKeyboardMarkup()
        texto="""Lo siento, no estás en un grupo autorizado."""
        config.bot.send_message(message.chat.id, text=texto, reply_markup=markup)
    else:
        if not usuario:
            markup  = types.InlineKeyboardMarkup()
            texto = config.mensajes["darse_de_alta"]
            markup.add(botones.getBoton("alta_usuario"))
            markup.add(botones.getBoton("cancelar"))
            config.bot.send_message(message.chat.id, text=texto, reply_markup=markup)
        elif message.chat.type=='group' or message.chat.type=='supergroup':
            config.bot.send_message(message.chat.id, text=config.mensajes["no_engorrines"], reply_to_message_id=message.id)
        else:
            flujoComun.dialogo_inicial(message.chat.id,usuario)


@config.bot.callback_query_handler(lambda call: call.data == "cancelar")
def adios (call):
    if call.message:
        config.bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,text=config.mensajes["adios"],reply_markup= types.InlineKeyboardMarkup())
    else:
        markup  = types.InlineKeyboardMarkup()
        config.bot.send_message(call.from_user.id, text=config.mensajes["adios"], reply_markup=markup)


while True:
    try:
        config.bot.polling(none_stop=True)
    except KeyboardInterrupt:
        print("Interrumpiendo Keyboard")
        sys.exit();
