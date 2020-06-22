# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config
import xml.etree.ElementTree as etree
# получаем настройки приложения
config = config.getConfig()
from loader import Loader

class PartHouse(Basic):
	name = "PartHouse"
	suppliers_id = 100
	warhouse_id = 19
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/PartHouse/"
	# пупустить строк в файле
	clearLine = 3
	# тип файла вложения
	parsertype = "zip"
	# тип файла прайса
	filetype = "csv"
	fileEncoding = "utf-8"
	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 0, "bra": 1, "price": 4, "quality": 3, "desc":2, "art_sup":0}

