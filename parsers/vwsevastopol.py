# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class VwSevastopol(Basic):
	name = "VwSevastopol"
	suppliers_id = 102
	warhouse_id = 175
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/VwSevastopol/"
	# делитель CSV
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xls"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 3, "price": 5, "quality": 4, "desc":2, "art_sup":3}

class VwSimferopol(Basic):
	name = "VwSimferopol"
	suppliers_id = 102
	warhouse_id = 159
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/VwSimferopol/"
	# делитель CSV
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xls"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 3, "price": 5, "quality": 4, "desc":2, "art_sup":3}















