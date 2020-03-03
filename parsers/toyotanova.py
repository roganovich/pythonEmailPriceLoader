# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Toyotanova(Basic):
	name = "Toyotanova"
	suppliers_id = 23
	warhouse_id = 27
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Toyotanova/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	# не ясный формат. excel
	filetype = "xls"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 0, "bra": 2, "price": 4, "quality": 3, "desc":1, "art_sup":0}















