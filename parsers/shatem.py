# author Roganovich.R.M.

from parsers.basic import Basic
import config

# получаем настройки приложения
config = config.getConfig()

class Shateminsk(Basic):
	name = "Shateminsk"
	suppliers_id = 56
	warhouse_id = 59
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Shateminsk/"
	# делитель CSV
	delimiter = ";"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "zip"
	# тип файла прайса
	filetype = "csv"
	fileEncoding = "windows-1251"

	# в файле [КатНомер	Наименование	Производитель	Применяемость	Кроссы	Цена	Наличие]
	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 6, "quality": 3, "desc":2, "art_sup":1}

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
	fileEncoding = "windows-1251"

	# в файле [КатНомер	Наименование	Производитель	Применяемость	Кроссы	Цена	Наличие]
	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 6, "quality": 3, "desc":2, "art_sup":1}

class Shateekat(Basic):
	name = "Shateekat"
	suppliers_id = 41
	warhouse_id = 18
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Shateekat/"
	# делитель CSV
	delimiter = ";"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "zip"
	# тип файла прайса
	filetype = "csv"
	fileEncoding = "windows-1251"

	# в файле [КатНомер	Наименование	Производитель	Применяемость	Кроссы	Цена	Наличие]
	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 6, "quality": 3, "desc":2, "art_sup":1}





class ShateminskTest(Basic):
	name = "ShateminskTest"
	suppliers_id = 82
	warhouse_id = 59
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/ShateminskTest/"
	# делитель CSV
	delimiter = ";"
	# пупустить строк в файле
	clearLine = 1
	# тип файла вложения
	parsertype = "zip"
	# тип файла прайса
	filetype = "csv"
	fileEncoding = "windows-1251"

	# в файле [КатНомер	Наименование	Производитель	Применяемость	Кроссы	Цена	Наличие]
	# сопостовляем колонки в файле с назначениями полей
	colums = {"art": 1, "bra": 0, "price": 6, "quality": 3, "desc":2, "art_sup":1}









