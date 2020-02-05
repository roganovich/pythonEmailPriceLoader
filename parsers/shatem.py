# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Shatem(Basic):
	name = "Shatem"
	suppliers_id = 40
	warhouse_id = 60
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Shatem/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "zip"
	# тип файла прайса
	filetype = "csv"
	fileEncoding = "utf-8"

	# в файле [КатНомер	Наименование	Производитель	Применяемость	Кроссы	Цена	Наличие]
	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 6, "quality": 3, "desc":3, "art_sup":1}














