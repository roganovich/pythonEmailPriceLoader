# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Tisrostov(Basic):
	name = "Tisrostov"
	suppliers_id = 108
	warhouse_id = 166
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Tisrostov/"
	# делитель CSV
	delimiter = "\t"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "zip"
	# тип файла прайса
	filetype = "xls"
	fileEncoding = "windows-1251"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 5, "quality": 4, "desc":2, "art_sup":3}
















