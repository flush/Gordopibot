from datetime import datetime, timedelta
from telebot import types
import config

def mostrarSelectorDuracion(chatId,messageId,userId):
    markup  = types.InlineKeyboardMarkup(row_width=4)
    sesion  = config.sesionHandler.getSesion(userId)
    filaBotones = []
    for x in range(config.config["minDuracion"],config.config["maxDuracion"]+1):
        filaBotones.append(types.InlineKeyboardButton(str(x)+" horas",
                                              callback_data="duracionelegida_"+str(x)))
        filaBotones.append(types.InlineKeyboardButton(str(x)+".5 horas",
                                                      callback_data="duracionelegida_"+str(x)+".5"))
    markup.add(*filaBotones)
    config.bot.edit_message_text(config.mensajes["elige_duracion_apertura"],chatId,messageId,reply_markup=markup)

def mostrarSelectorHora(chatId,messageId,userId):
    markup  = types.InlineKeyboardMarkup(row_width=4)
    sesion  = config.sesionHandler.getSesion(userId)
    filaBotones = []
    minHora = sesion.minHoraSelector
    maxHora = sesion.maxHoraSelector
    #Si estamos elegiendo la hora de una partida y la hora de cierre del local no es a en punto
    # dejamos elegir la última hora
    if sesion.maxMinutoSelector is  not None  and  sesion.maxMinutoSelector > 0:
        maxHora = maxHora +1 
    for x in range(minHora,maxHora):
        filaBotones.append(types.InlineKeyboardButton(str(x)+":00",
                                              callback_data="horaelegida_"+str(x)))
    markup.add(*filaBotones)
    config.bot.edit_message_text(config.mensajes["elige_hora_apertura"],chatId,messageId,reply_markup=markup)

def mostrarSelectorMinutos(chatId,messageId,userId,hora):
    markup  = types.InlineKeyboardMarkup(row_width=4)
    sesion  = config.sesionHandler.getSesion(userId)
    horaMin = 0
    horaMax = 10000
    filaBotones = []
    if sesion.minMinutoSelector:
            horaMin = sesion.minHoraSelector*100+sesion.minMinutoSelector
            horaMax = sesion.maxHoraSelector*100+sesion.maxMinutoSelector
    for x in range(0,46,15):
        horaNum = hora*100+x;
        if horaMin <= horaNum <horaMax:
            filaBotones.append(types.InlineKeyboardButton(str(hora)+":"+f"{x:02}",callback_data="minutoelegido_"+str(x)))
    markup.add(*filaBotones)
    config.bot.edit_message_text(config.mensajes["elige_minutos_apertura"],chatId,messageId,reply_markup=markup)

def mostrarSelectorDia(chatId,messageId):
    markup  = types.InlineKeyboardMarkup()
    fechaActual = datetime.now().replace(hour=0,minute=0,second=0)
    for x in range(config.config["maxDiasFuturoReserva"]):
        fechaDia = fechaActual + timedelta(days=x)
        markup.add(types.InlineKeyboardButton(fechaDia.strftime("%A %d de %B"),
                                              callback_data="diaelegido_"+str(fechaDia.timestamp())))

    config.bot.edit_message_text(config.mensajes["elige_fecha_apertura"],chatId,messageId,reply_markup=markup)




@config.bot.callback_query_handler(lambda call: call.data.startswith("diaelegido"))
def diaElegido(call):

  diaElegido = datetime.fromtimestamp(float(call.data.split("_")[1]))
  sesion  = config.sesionHandler.getSesion(call.from_user.id)
  sesion.diaElegido = diaElegido
  mostrarSelectorHora(call.message.chat.id,call.message.id,call.from_user.id)
    
@config.bot.callback_query_handler(lambda call: call.data.startswith("horaelegida"))
def horaElegida(call):

  hora_elegida = int(call.data.split("_")[1])
  sesion  = config.sesionHandler.getSesion(call.from_user.id)
  if hora_elegida==24:
      hora_elegida = 0
  sesion.diaElegido = sesion.diaElegido.replace(hour=hora_elegida)
  mostrarSelectorMinutos(call.message.chat.id,call.message.id,call.from_user.id,hora_elegida)  

@config.bot.callback_query_handler(lambda call: call.data.startswith("minutoelegido"))    
def minutoElegido(call):
  minuto_elegido = int(call.data.split("_")[1])
  sesion  = config.sesionHandler.getSesion(call.from_user.id)
  sesion.diaElegido = sesion.diaElegido.replace(minute=minuto_elegido)
  if sesion.elegirDuracion == True:
      mostrarSelectorDuracion(call.message.chat.id, call.message.id,call.from_user.id)
  else:
      sesion.calendarCallBack(call.message.chat.id, call.message.id,call.from_user.id)


@config.bot.callback_query_handler(lambda call: call.data.startswith("duracionelegida"))    
def finSeleccion(call):
  duracion_elegida = float(call.data.split("_")[1])
  sesion  = config.sesionHandler.getSesion(call.from_user.id)
  sesion.duracionElegida = duracion_elegida
  sesion.calendarCallBack(call.message.chat.id, call.message.id,call.from_user.id)
  

