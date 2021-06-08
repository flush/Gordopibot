import config
import calendario
from telebot import types
from datetime import  timedelta
import botones
from boardgamegeek import BGGClient
from multiprocessing import Pool

@config.bot.callback_query_handler(lambda call: call.data == "crear_partida")
def crearPartida(call):
    markup  = types.InlineKeyboardMarkup()
    aperturas = config.aperturaDB.getAperturas()
    if len(aperturas) > 0 :
        for apertura in aperturas:
            texto = apertura.fechaApertura.strftime("A %d de %B a las %H:%M") +"-" + apertura.fechaCierre.strftime("%H:%M")
            markup.add(types.InlineKeyboardButton(texto,switch_inline_query_current_chat="buscarJuego",callback_data="sesionelegida_"+str(apertura.id)))
        markup.add(botones.getBoton("cancelar"))
        config.bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,text=config.mensajes["elegir_sesion"],reply_markup=markup)
    else:
        config.bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,text=config.mensajes["sin_sesiones_abiertas"])


@config.bot.callback_query_handler(lambda call: call.data.startswith("sesionelegida"))
def sesionElegida(call):
    idApertura = call.data.split("_")[1]
    sesion = config.sesionHandler.getSesion(call.from_user.id)
    sesion.idApertura = idApertura
    markup  = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("OK",switch_inline_query_current_chat=""))
    markup.add(botones.getBoton("cancelar"))
    config.bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,text=config.mensajes["buscar_juegos"],reply_markup=markup)
    #elegirJuego(call.message.chat.id,call.message.id,call.from_user.id);


def getDetalleJuego(juego):
    return  BGGClient().game(game_id=juego.id);
    
@config.bot.inline_handler(lambda query: True) 
def elegirJuego(inline_query):
    if len(inline_query.query.strip()) == 0:
        config.bot.answer_inline_query(inline_query.id,[])
    else:
        juegos = BGGClient().search("arkham",("boardgame",))
        opciones = []
        p = Pool(20)
        juegosDetallados =p(getDetalleJuego,juegos)
        for juego in juegosDetallados:
            opciones.append(types.InlineQueryResultArticle(id=juego.id,title=juego.name,input_message_content=types.InputTextMessageContent(juego.description),thumb_url=juego.thumbnail))
        config.bot.answer_inline_query(inline_query.id,opciones[0:20])

        


    
