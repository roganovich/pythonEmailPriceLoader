# author Roganovich.R.M.

from parsers.basic import Basic
import config
import shutil
import os
import requests

# получаем настройки приложения
config = config.getConfig()

class Kulisa(Basic):
	name = "Kulisa"
	suppliers_id = 105
	warhouse_id = 162
	data = []
	email = {}
	# путь к каталогу с файлами
	filePathExtract = "files/Kulisa/"
	# пупустить строк в файле
	clearLine = 0
	# тип файла вложения
	parsertype = "file"
	# тип файла прайса
	filetype = "csv"

	# сопостовляем колонки в файле с назначениями полей
	# price_dop1 - розница и дискот 5
	# price_dop2 - закупочная цена
	# price_dop3 - дисконт 1 и 3
	colums = {"art": 0, "bra": 2, "price": 4, "quality": 1, "desc":3, "art_sup":0}


	def downloadFiles(self):
		self.email['email_from'] = "bahchisaray.myserv.top"
		url = 'http://bahchisaray.myserv.top:44000/kulisa_ostatki.txt';
		path = self.getParserPath()
		filePath = path + 'price.csv'
		myfile = requests.get(url)
		open(filePath, 'wb').write(myfile.content)

