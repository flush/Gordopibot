import telebot
import json, ssl
from telebot import types
import time
import mariadb
from pathlib import Path
from os import path, remove
from usuariosBO import UsuarioDB
from aperturasBO import AperturasDB
from sesiones import SesionHandler
import locale

global sesiones
global config
global mensajes
global bot
global sesionHandler
global pool
global usuarioDB


#for lang in locale.locale_alias.values():
#    print(lang)

locale.setlocale(locale.LC_ALL,"es_ES.utf-8")
sesiones = {}
#Finding the absolute path of the config file
scriptPath =path.abspath('__file__')
dirPath = path.dirname(scriptPath)
configPath = path.join(dirPath,'config.json')
#Se leen los archivos de configuracion y de cadenas
config = json.load(open(configPath))
mensajes = json.load(open(path.join(dirPath,'mensajes.json')))
print(config["botToken"])
bot = telebot.TeleBot(config["botToken"],parse_mode="HTML")
#creación del pool de conexión
dbconfig = config['database']
sesionHandler = SesionHandler(config['sesionTimeout'])
pool = mariadb.ConnectionPool(**dbconfig)
usuarioDB = UsuarioDB(pool)
aperturasDB = AperturasDB(pool)


