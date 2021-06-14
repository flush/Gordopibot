import config
import calendario
from telebot import types
from datetime import  timedelta
import botones

@config.bot.callback_query_handler(lambda call: call.data.startswith("que_se_cuece"))
def queSeCuece(call):
    respuesta =config.mensajes["esto_montado"]
    aperturas = config.aperturaDB.getAperturas()
    partidas = config.partidasDB.getPartidas()
    if len(aperturas) == 0:
        respuesta= config.mensajes["nada_montado"]
    else:
        for apertura in aperturas:
            respuesta +="<u><b>"+apertura.toString() +"</b></u>\n"
            ningunapartida=True
            for partida in partidas:
                if partida.idApertura == apertura.id:
                    ningunapartida=False
                    usuarios = config.partidasDB.getUsuariosApuntados(partida.id)
                    strUsuarios="["
                    first=True
                    for usuario in usuarios:
                        if not first:
                            strUsuarios+=','
                        first = False
                        strUsuarios += usuario.nombre
                    strUsuarios+=']'
                        
                    respuesta+=  partida.resumen() +" "+strUsuarios+"\n"
            if ningunapartida == True:
                respuesta+=config.mensajes["sin_partidas"]+"\n"
    config.bot.edit_message_text(chat_id= call.message.chat.id,message_id = call.message.id,text=respuesta)



@config.bot.callback_query_handler(lambda call: call.data.startswith("aperturairlocal"))
@config.requiere_sesion
def sesionElegida(call):
    idApertura = call.data.split("_")[1]
    sesion = config.sesionHandler.getSesion(call.from_user.id)
    resultado = config.aperturaDB.apuntarASesion(call.from_user.id,idApertura)
    print(resultado)
    config.bot.edit_message_text(chat_id= call.message.chat.id,message_id = call.message.id,text=config.mensajes[resultado.value])



    


@config.bot.callback_query_handler(lambda call: call.data == "ir_local")
@config.requiere_sesion
def irLocal(call):
    markup  = types.InlineKeyboardMarkup()
    aperturas = config.aperturaDB.getAperturas()
    if len(aperturas) > 0 :
        for apertura in aperturas:
            texto = apertura.fechaApertura.strftime("A %d de %B a las %H:%M") +"-" + apertura.fechaCierre.strftime("%H:%M")
            markup.add(types.InlineKeyboardButton(texto,callback_data="aperturairlocal_"+str(apertura.id)))
        markup.add(botones.getBoton("cancelar"))
        config.bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,text=config.mensajes["elegir_sesion_ir"],reply_markup=markup)
    else:
        config.bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,text=config.mensajes["sin_sesiones_abiertas"])


@config.bot.callback_query_handler(lambda call: call.data == "abrir_local")
@config.requiere_sesion
def abrirLocal(call):
    sesion = config.sesionHandler.getSesion(call.from_user.id)
    sesion.calendarCallBack = confirmarFechaHora
    sesion.minHoraSelector = config.config["minHoraApertura"]
    sesion.maxHoraSelector = config.config["maxHoraApertura"] + 1
    sesion.minMinutoSelector = None
    sesion.maxMinutoSelector = None
    sesion.elegirDuracion = True
    calendario.mostrarSelectorDia(call.message.chat.id,call.message.id)

def confirmarFechaHora(chatId,messageId,userId):
    sesion  = config.sesionHandler.getSesion(userId)
    markup  = types.InlineKeyboardMarkup()
    diaHora = sesion.diaElegido.strftime("%A %d de %B a las %H:%M")
    finApertura = (sesion.diaElegido +timedelta(hours=sesion.duracionElegida)).strftime("%H:%M")
    markup.add(botones.getBoton("confirmar_apertura"))
#    markup.add(botones.getBoton("confirmar_apertura_partida"))
    markup.add(botones.getBoton("cancelar"))    
    config.bot.edit_message_text(message_id=messageId, chat_id= chatId,
                                 text=config.mensajes["confirmar_fecha_apertura"].format(diaElegido=diaHora,finApertura=finApertura)
                                 ,reply_markup=markup)

@config.bot.callback_query_handler(lambda call: call.data.startswith("confirmar_apertura"))
@config.requiere_sesion
def guardarApertura(call):
    sesion  = config.sesionHandler.getSesion(call.from_user.id)
    inicioApertura =  sesion.diaElegido
    finApertura = sesion.diaElegido +timedelta(hours=sesion.duracionElegida)
    sesion.apertura = config.aperturaDB.insertarApertura(call.from_user.id,inicioApertura,finApertura)
    config.aperturaDB.apuntarASesion(call.from_user.id,sesion.apertura.id)
    
    inicioAperturaStr = sesion.diaElegido.strftime("%A %d de %B a las %H:%M")
    finAperturaStr = (sesion.diaElegido +timedelta(hours=sesion.duracionElegida)).strftime("%H:%M")
    sesion.diaElegido = None
    sesion.finApertura = None
    if call.data == "confirmar_apertura":
        config.bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,
                                     text=config.mensajes["apertura_creada"].format(inicioApertura=inicioAperturaStr,
                                                                                    finApertura=finAperturaStr),
                                     reply_markup= types.InlineKeyboardMarkup())

