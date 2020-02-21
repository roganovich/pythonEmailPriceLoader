# author Roganovich.R.M.
import os
import log
import csv
import datetime
from loader import Loader
from parsers.basic import Basic
import config
# получаем настройки приложения
config = config.getConfig()


class Satrade(Basic):
	name = "Satrade"
	suppliers_id = 30
	warhouse_id = 38
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Satrade/"
	# пупустить строк в файле
	clearLine = 3
	# тип файла вложения
	parsertype = "rar"
	# тип файла прайса
	filetype = "xls"

	# в файле ['Артикул', 'Бренд', 'Окончательная цена', 'Количество', 'Наименование номенклатуры', 'Полный артикул']
	# сопостовляем колонки в файле с назначениями полей
	colums ={"art": 0, "bra": 3, "price": 7, "quality": 8, "desc": 2, "art_sup":3}











