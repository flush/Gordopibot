import config
import botones
import gruposHelper 
import flujoComun

@config.bot.callback_query_handler(lambda call: call.data == "alta_socio_pago")
def alta_socio_pago(call):
    usuario = config.usuarioDB.insertarUsuario(call.from_user.id,getNombreUsuario(call.from_user),"SP")
    flujoComun.dialogo_inicial(call.message.chat.id,usuario)

    
@config.bot.callback_query_handler(lambda call: call.data == "alta_socio_junior")
def alta_socio_junior(call):
    usuario = config.usuarioDB.insertarUsuario(call.from_user.id,getNombreUsuario(call.from_user),"SJ")    
    flujoComun.dialogo_inicial(call.message.chat.id,usuario)    

@config.bot.callback_query_handler(lambda call: call.data == "alta_usuario")
def alta_usuario(call):
    if gruposHelper.vieneDeJugones(call.message.chat.id):
        usuario = config.usuarioDB.insertarUsuario(call.from_user.id,getNombreUsuario(call.from_user),"JU")    
        flujoComun.dialogo_inicial(call.message.chat.id,usuario);
    else:
          config.bot.edit_message_text(message_id=call.message.id, chat_id= call.message.chat.id,
                                text=config.mensajes["tipo_socio"],
                                reply_markup=botones.getTeclado("alta_socio_pago","alta_socio_junior","cancelar"))

def getNombreUsuario(fromUser):
    nombre = fromUser.username;

    if nombre is None:
        nombre = fromUser.first_name;
        if not fromUser.last_name is None:
            nombre = nombre +" " +fromUser.last_name
    return nombre

          
