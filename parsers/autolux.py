# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Autolux(Basic):
	name = "Autolux"
	suppliers_id = 103
	warhouse_id = 160
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Autolux/"
	# пупустить строк в файле
	clearLine = 2
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xls"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 3, "bra": 2, "price": 6, "quality": 5, "desc":4, "art_sup":1}















