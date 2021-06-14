import config
import traceback
import calendario
from telebot import types
from datetime import  timedelta
import botones
import util
from boardgamegeek import BGGClient
from partidasBO import Partida
from multiprocessing import Pool
from flujoComun import ResultadoApuntar

@config.bot.callback_query_handler(lambda call: call.data == "crear_partida")
@config.requiere_sesion
def crearPartida(call):
    markup  = types.InlineKeyboardMarkup()
    aperturas = config.aperturaDB.getAperturas()
    if len(aperturas) > 0 :
        for apertura in aperturas:
            texto = apertura.fechaApertura.strftime("A %d de %B a las %H:%M") +"-" + apertura.fechaCierre.strftime("%H:%M")
            markup.add(types.InlineKeyboardButton(texto,callback_data="sesionelegida_"+str(apertura.id)))
        markup.add(botones.getBoton("cancelar"))
        config.bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,text=config.mensajes["elegir_sesion"],reply_markup=markup)
    else:
        config.bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,text=config.mensajes["sin_sesiones_abiertas"])

def horapartidaElegida(chatId,messageId,userId):

    sesion = config.sesionHandler.getSesion(userId)
    sesion.fechaPartida = sesion.diaElegido
    markup  = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("OK",switch_inline_query_current_chat=""))
    markup.add(botones.getBoton("cancelar"))
    sesion.deleteChatId = chatId
    sesion.deleteMessageId = messageId
    config.bot.edit_message_text(message_id=messageId, chat_id=chatId,text=config.mensajes["buscar_juegos"],reply_markup=markup)


@config.bot.callback_query_handler(lambda call: call.data.startswith("sesionelegida"))
@config.requiere_sesion
def sesionElegida(call):
    idApertura = call.data.split("_")[1]
    sesion = config.sesionHandler.getSesion(call.from_user.id)
    sesion.apertura = config.aperturaDB.getApertura(idApertura);
    sesion.diaElegido = sesion.apertura.fechaApertura
    sesion.elegirDuracion = False
    sesion.calendarCallBack = horapartidaElegida
    markup  = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("OK",switch_inline_query_current_chat=""))
    markup.add(botones.getBoton("cancelar"))
    sesion.deleteChatId = call.message.chat.id
    sesion.deleteMessageId = call.message.id
    sesion.minHoraSelector = sesion.apertura.fechaApertura.hour
    sesion.minMinutoSelector = sesion.apertura.fechaApertura.minute
    sesion.maxHoraSelector = sesion.apertura.fechaCierre.hour
    if sesion.maxHoraSelector == 0:
        sesion.maxHoraSelector = 24
    sesion.maxMinutoSelector = sesion.apertura.fechaCierre.minute
    calendario.mostrarSelectorHora(call.message.chat.id,call.message.id,call.from_user.id)

    


    

def getDetalleJuego(juego):

    try:
        juegoDetalle=  BGGClient().game(game_id=juego.id);
        juegoDetalle.nombre = juego.name
        return juegoDetalle
    except:
        juego.thumbnail = ""
        juego.nombre = juego.name
        return juego
    
    
@config.bot.inline_handler(lambda query: True)
@config.requiere_sesion
def elegirJuego(inline_query):
    if len(inline_query.query.strip()) == 0:
        config.bot.answer_inline_query(inline_query.id,[])
    else:
        offset = 0

        if inline_query.offset != "":
            offset = int(inline_query.offset)
            
        sesion = config.sesionHandler.getSesion(inline_query.from_user.id)
        sesion.cadenaBusquedaJuego = util.quitarAcentos(inline_query.query.strip().lower())

        juegos = BGGClient().search(inline_query.query.strip(),("boardgame",))

        opciones = []
        p = Pool(10)
        juegosDetallados =p.map(getDetalleJuego,juegos[offset:offset+10])
        markup  = botones.getTeclado("boton_quieto");
        sesion.listadoJuegos = juegosDetallados

        for juego in juegosDetallados:
            if juego:
                opciones.append(types.InlineQueryResultArticle(id=juego.id,title=juego.nombre,input_message_content=types.InputTextMessageContent(config.mensajes['esperando']),thumb_url=juego.thumbnail,reply_markup=markup))
        config.bot.answer_inline_query(inline_query.id,opciones,cache_time=0,next_offset=offset+10)

        

@config.bot.chosen_inline_handler(func=lambda chosen_inline_result: True)
@config.requiere_sesion
def test_chosen(result):
    juegoDetalle=  BGGClient().game(game_id=result.result_id);
    sesion = config.sesionHandler.getSesion(result.from_user.id)
    markup  = types.InlineKeyboardMarkup()



    
    
    nombreJuego = juegoDetalle.name
    for nombre in juegoDetalle.alternative_names:
        nombreSinAcentos = util.quitarAcentos(nombre.lower())
        if  nombreSinAcentos.find(sesion.cadenaBusquedaJuego) >= 0:
            nombreJuego = nombre
    sesion.partida = Partida(None,sesion.fechaPartida,nombreJuego,result.result_id,sesion.apertura.id,result.from_user.id,juegoDetalle.max_players)

    for x in range(juegoDetalle.max_players,juegoDetalle.min_players-1,-1):
            markup.add(types.InlineKeyboardButton(config.mensajes["partida_confirmada"]+" "+str(x)+" plazas.",callback_data="confirmarpartida_"+str(x)))
        
    markup.add(botones.getBoton("cancelar"))
    texto  = config.mensajes["confirmar_partida"].format(fechaPartida=sesion.fechaPartida.strftime("%A %d de %B a las %H:%M"),nombreJuego=nombreJuego,
                                                                                                  minJug=juegoDetalle.min_players,maxJug=juegoDetalle.max_players)
    sesion.fechaPartida = None


    config.bot.edit_message_text(inline_message_id=result.inline_message_id, text=texto, reply_markup=markup)



@config.bot.callback_query_handler(lambda call: call.data.startswith("confirmarpartida"))
@config.requiere_sesion
def guardarPartida(call):

    plazas = call.data.split("_")[1]
    sesion = config.sesionHandler.getSesion(call.from_user.id)
    sesion.partida.plazas = int(plazas)
    texto=""
    if config.aperturaDB.getPlazasLibres(sesion.partida.idApertura) > 0 or config.aperturaDB.estaUsuarioApuntado(sesion.partida.idApertura,call.from_user.id):
        config.partidasDB.insertarPartida(sesion.partida)
        config.partidasDB.apuntarAPartida(call.from_user.id,sesion.partida.id)
        texto = "partida_guardada"
    else:
        texto = "sin_aforo"

    sesion.partida = None
    sesion.apertura = None

    config.bot.edit_message_text(inline_message_id=call.inline_message_id, text=config.mensajes[texto])
    config.bot.delete_message(sesion.deleteChatId,sesion.deleteMessageId)
        




@config.bot.callback_query_handler(lambda call: call.data.startswith("partidaelegida"))
@config.requiere_sesion
def partida_elegida(call):
    sesion = config.sesionHandler.getSesion(call.from_user.id)
    idPartida  = call.data.split("_")[1]
    resultado = config.partidasDB.apuntarAPartida(call.from_user.id,idPartida)
    texto = config.mensajes[resultado.value]
#    if resultado == ResultadoApuntar.OK_PARTIDA:

    config.bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text=texto)

    
@config.bot.callback_query_handler(lambda call: call.data =="unirse_partida")
@config.requiere_sesion
def elegir_partida(call):
    sesion = config.sesionHandler.getSesion(call.from_user.id)
    partidas = config.partidasDB.getPartidas();
    markup  = types.InlineKeyboardMarkup()
    markup.row_width=1
    botonesPartidas= []
    for partida in partidas:
        if config.partidasDB.getPlazasLibres(partida.id)>0:
            botonesPartidas.append(types.InlineKeyboardButton(partida.toString(),callback_data="partidaelegida_"+str(partida.id)))
    if len(botonesPartidas) > 0:
        botonesPartidas.append(botones.getBoton("cancelar"))
        markup.add(*botonesPartidas)
        config.bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text=config.mensajes["listado_partidas"],reply_markup=markup)
    else:
        config.bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text=config.mensajes["no_hay_partidas"])


    
    
            

    
    

   


        


   
 
