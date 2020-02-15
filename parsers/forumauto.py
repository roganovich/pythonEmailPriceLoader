# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class ForumAuto(Basic):
	name = "ForumAuto"
	suppliers_id = 83
	warhouse_id = 115
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/ForumAuto/"
	# делитель CSV
	delimiter = ";"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "zip"
	# тип файла прайса
	filetype = "csv"
	fileEncoding = "windows-1251"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 3, "quality": 4, "desc":2, "art_sup":1}















