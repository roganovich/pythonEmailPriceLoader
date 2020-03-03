# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class PFLRostov(Basic):
	name = "PFLRostov"
	suppliers_id = 69
	warhouse_id = 96
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/PFLRostov/"
	# делитель CSV
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xlsx"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 5, "quality": 6, "desc":2, "art_sup":3}

class PFLKrasnodar(Basic):
	name = "PFLKrasnodar"
	suppliers_id = 69
	warhouse_id = 98
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/PFLKrasnodar/"
	# делитель CSV
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xlsx"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 5, "quality": 6, "desc":2, "art_sup":3}















