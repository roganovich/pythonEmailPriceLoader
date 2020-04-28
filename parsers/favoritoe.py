# author Roganovich.R.M.
import os
import log
from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Favoritoe(Basic):
	name = "Favoritoe"
	suppliers_id = 114
	warhouse_id = 171
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Favoritoe/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xlsx"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 3, "quality": 4, "desc":2, "art_sup":1}














