import config
def vieneDeJugones(idChat):
    return idChat == config.config["idGrupoJugones"]

def vieneDeSocios(idChat):
    return idChat == config.config["idGrupoSocios"]

def grupoAutorizado(idChat):
    return vieneDeSocios(idChat) or vieneDeJugones(idChat)
