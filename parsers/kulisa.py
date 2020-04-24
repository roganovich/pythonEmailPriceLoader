# author Roganovich.R.M.

from parsers.basic import Basic
import config
import shutil
import os
import urllib3

# получаем настройки приложения
config = config.getConfig()

class Kulisa(Basic):
	name = "Kulisa"
	suppliers_id = 105
	warhouse_id = 162
	data = []
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
		url = 'http://bahchisaray.myserv.top:44000/kulisa_ostatki.txt';
		path = self.getParserPath()
		filePath = path + 'price.csv'
		with open(filePath, 'w', encoding='utf-8') as f_out:
			f_out.write(self.file_get_contents(url))
		exit()



	def file_get_contents(self, url):
		http = urllib3.PoolManager()
		r = http.request('GET', 'http://httpbin.org/robots.txt')
		return r.data


