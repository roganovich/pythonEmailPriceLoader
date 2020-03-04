# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Voltag(Basic):
	name = "Voltag"
	suppliers_id = 112
	warhouse_id = 169
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Voltag/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xls"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 0, "bra": 1, "price": 2, "quality": 3, "desc":4, "art_sup":0}






