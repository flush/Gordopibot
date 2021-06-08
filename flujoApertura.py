import config
import calendario
from telebot import types
from datetime import  timedelta
import botones

@config.bot.callback_query_handler(lambda call: call.data == "abrir_local")
def abrirLocal(call):
    sesion = config.sesionHandler.getSesion(call.from_user.id)
    sesion.calendarCallBack = confirmarFechaHora
    sesion.minHoraSelector = config.config["minHoraApertura"]
    sesion.maxHoraSelector = config.config["maxHoraApertura"] + 1
    calendario.mostrarSelectorDia(call.message.chat.id,call.message.id)

def confirmarFechaHora(chatId,messageId,userId):
    sesion  = config.sesionHandler.getSesion(userId)
    markup  = types.InlineKeyboardMarkup()
    diaHora = sesion.diaElegido.strftime("%A %d de %B a las %H:%M")
    finApertura = (sesion.diaElegido +timedelta(hours=sesion.duracionElegida)).strftime("%H:%M")
    markup.add(botones.getBoton("confirmar_apertura"))
    markup.add(botones.getBoton("confirmar_apertura_partida"))
    markup.add(botones.getBoton("cancelar"))    
    config.bot.edit_message_text(message_id=messageId, chat_id= chatId,
                                 text=config.mensajes["confirmar_fecha_apertura"].format(diaElegido=diaHora,finApertura=finApertura)
                                 ,reply_markup=markup)

@config.bot.callback_query_handler(lambda call: call.data.startswith("confirmar_apertura"))
def guardarApertura(call):
    sesion  = config.sesionHandler.getSesion(call.from_user.id)
    inicioApertura =  sesion.diaElegido
    finApertura = sesion.diaElegido +timedelta(hours=sesion.duracionElegida)
    config.aperturaDB.insertarApertura(call.from_user.id,inicioApertura,finApertura)
    inicioAperturaStr = sesion.diaElegido.strftime("%A %d de %B a las %H:%M")
    finAperturaStr = (sesion.diaElegido +timedelta(hours=sesion.duracionElegida)).strftime("%H:%M")
    sesion.diaElegido = None
    sesion.finApertura = None
    if call.data == "confirmar_apertura":
        config.bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,
                                     text=config.mensajes["apertura_creada"].format(inicioApertura=inicioAperturaStr,
                                                                                    finApertura=finAperturaStr),
                                     reply_markup= types.InlineKeyboardMarkup())

