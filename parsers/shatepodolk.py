# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Shatepodolsk(Basic):
	name = "Shatepodolsk"
	suppliers_id = 41
	warhouse_id = 60
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Shatepodolsk/"
	# делитель CSV
	delimiter = ";"
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














