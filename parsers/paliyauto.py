# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Paliyauto(Basic):
	name = "Paliyauto"
	suppliers_id = 120
	warhouse_id = 183
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Paliyauto/"
	# делитель CSV
	delimiter = ";"
	# пупустить строк в файле
	clearLine = 4
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xlsx"

	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 5, "quality": 3, "desc":2, "art_sup":1}















