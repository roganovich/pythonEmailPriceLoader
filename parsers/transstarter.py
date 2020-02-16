# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Transstarter(Basic):
	name = "Transstarter"
	suppliers_id = 116
	warhouse_id = 176
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Transstarter/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xlsx"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 2, "bra": 4, "price": 6, "quality": 5, "desc":1, "art_sup":2}















