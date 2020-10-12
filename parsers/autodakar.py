# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class AutoDakar(Basic):
	name = "AutoDakar"
	suppliers_id = 96
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/AutoDakar/"
	# пупустить строк в файле
	clearLine = 0
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xlsx"
	fileEncoding = "utf-8"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 5, "quality": 4, "desc":2, "art_sup":1}

	#находим файл склада по созвучую названия
	unity= {
		"Fast-": "145", #//Dubai 20
		"48H-": "146", #Dubai 18
	}















