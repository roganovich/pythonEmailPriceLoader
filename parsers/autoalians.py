# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Autoalians(Basic):
	name = "Autoalians"
	suppliers_id = 119
	warhouse_id = 179
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Autoalians/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xlsx"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 4, "quality": 3, "desc":2, "art_sup":1}















