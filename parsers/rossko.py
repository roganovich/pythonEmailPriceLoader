# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config
import xml.etree.ElementTree as etree
# получаем настройки приложения
config = config.getConfig()
from loader import Loader

class Rossko(Basic):
	name = "Rossko"
	suppliers_id = 124
	warhouse_id = 189
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Rossko/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "zip"
	# тип файла прайса
	filetype = "xlsx"
	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 2, "bra": 1, "price": 6, "quality": 8, "desc":3, "art_sup":2}




