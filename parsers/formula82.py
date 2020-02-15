# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Formula82(Basic):
	name = "Formula82"
	suppliers_id = 130
	warhouse_id = 197
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Formula82/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xlsx"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 0, "bra": 4, "price": 2, "quality": 3, "desc":1, "art_sup":0}















