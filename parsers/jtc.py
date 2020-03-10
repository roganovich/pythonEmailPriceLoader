# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Jtc(Basic):
	name = "Jtc"
	suppliers_id = 95
	warhouse_id = 144
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Jtc/"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "xlsx"

	# сопостовляем колонки в файле с назначениями полей
	# price_dop1 - розница и дискот 5
	# price_dop2 - закупочная цена
	# price_dop3 - дисконт 1 и 3
	colums = {"art": 3, "bra": 0, "price": 4, "quality": 2, "desc":1, "art_sup":2, "price_dop1": 4, "price_dop2": 5, "price_dop3": 6}






