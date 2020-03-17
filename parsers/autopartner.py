# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Autopartner(Basic):
	name = "Autopartner"
	suppliers_id = 125
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Autopartner/"
	# пупустить строк в файле
	clearLine = 10
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xlsx"
	fileEncoding = "utf-8"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 4, "quality": 3, "desc":2, "art_sup":1}

	#находим файл склада по созвучую названия
	unity= {
		"Севастополь": "190",
		"Симферополь": "191",
	}















