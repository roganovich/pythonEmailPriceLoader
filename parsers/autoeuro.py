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


class Autoeuro(Basic):
	name = "Autoeuro"
	suppliers_id = 65
	warhouse_id = 125
	data = []
	# путь к каталогу с файлами
	filePathExtract = "files/Autoeuro/"
	# делитель CSV
	delimiter = "\t"
	# пупустить первую строку в файле
	firstLine = True
	# тип файла вложения
	parsertype = "rar"
	# тип файла прайса
	filetype = "csv"

	# в файле ['Артикул', 'Бренд', 'Окончательная цена', 'Количество', 'Наименование номенклатуры', 'Полный артикул']
	# сопостовляем колонки в файле с назначениями полей
	colums ={"art": 0, "bra": 1, "price": 2, "quality": 3, "desc": 4, "art_sup":5}











