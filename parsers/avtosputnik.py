# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Avtosputnik(Basic):
	name = "Avtosputnik"
	suppliers_id = 63
	warhouse_id = 90
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Avtosputnik/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "zip"
	# тип файла прайса
	filetype = "xml"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 0, "bra": 1, "price": 3, "quality": 4, "desc":2, "art_sup":0}






