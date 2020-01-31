# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Focusauto(Basic):
	name = "Focusauto"
	suppliers_id = 129
	warhouse_id = 196
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Focusauto/"
	# пупустить первую строку в файле
	firstLine = True
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xls"
	fileEncoding = "utf-8"

	# в файле [КатНомер	Наименование	Производитель	Применяемость	Кроссы	Цена	Наличие]
	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 0, "bra": 1, "price": 4, "quality": 3, "desc":2, "art_sup":0}














