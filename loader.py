import log
import os
import config
import datetime
import csv
import psycopg2
import re

# получаем настройки приложения
config = config.getConfig()

class Loader:
	# конструктор
	def __init__(self, obj):
		self.obj = obj
		self.war_id= str(obj.warhouse_id)
		self.sup_id = str(obj.suppliers_id)

		dateCreate = str(datetime.datetime.today().strftime("%Y%m%d"))
		resultPath = config.get("email","resultsFolder") + '/' + dateCreate + '/' + self.sup_id + '/' + self.war_id + '/'
		self.file_path = os.path.join(self.obj.basePath, resultPath)
		self.file_name = "price.csv"
		# если не существует дириктории создаем ее
		if (not os.path.exists(self.file_path)):
			log.print_r('Создаю директорию ' + self.file_path)
			os.makedirs(self.file_path)
		# путь к записи файла
		self.resultFilePath = self.file_path + self.file_name
		# открываем файл результата
		self.resultFile = open(self.resultFilePath, 'a', newline='', encoding='utf-8')
		self.writer = csv.writer(self.resultFile, delimiter='\t')
		self.createPricesFile()
		self.conn = psycopg2.connect(dbname=config.get("pgconfig","dbname"), user=config.get("pgconfig","user"),password=config.get("pgconfig","password"), host=config.get("pgconfig","host"))
		self.cursor = self.conn.cursor()
		log.print_r('Открыл соединение с '+config.get("pgconfig","dbname"))

	# функция создает новую запись в prices_file
	def createPricesFile(self):
		#2020-02-04 11:30:12
		# создаем ид файла загрузки
		createtime = str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
		query = ("INSERT INTO public.prices_file(prf_email_from, prf_sup_id, prf_war_id, prf_createtime, status)VALUES (%s, %s, %s, %s, %s) RETURNING prf_id")
		data = (self.obj.email['email_from'],self.sup_id,self.war_id, createtime, 0)
		self.cursor.execute(query, data)
		self.prf_id = self.cursor.fetchone()[0]
		self.conn.commit()

	def validate(self, data):
		log.print_r(data)
		# подготавливаем поля для записи
		prfc_prices_file_id = self.prf_id
		prfc_article = re.sub(r'[^0-9A-Za-z\s+]+', r'', str(data[0]).strip())
		prfc_brand = re.sub(r'[^0-9A-Za-zа-яА-ЯёЁ\-\s+]+', r'', str(data[1]).strip())

		priceClaer = re.sub(r'[^0-9.]+', r'', str(data[2]).strip().replace(',', '.'))
		if (self.is_number(priceClaer)):
			prfc_price = round(float(priceClaer), 2)
		else:
			return False
		qualityClaer = re.sub(r'[^0-9.]+', r'', str(data[3]).strip().replace(',', '.'))
		if (self.is_number(qualityClaer)):
			prfc_quality = round(float(qualityClaer))
		else:
			return False

		return {'prfc_prices_file_id':str(prfc_prices_file_id),'prfc_article':str(prfc_article),'prfc_brand':str(prfc_brand),'prfc_price':str(prfc_price),'prfc_quality':str(prfc_quality)}

	# функция ищет бренд, артикул, очищает остатки, цены и записывает новые
	def writerests(self, data):
		log.print_r(data)
		query = ("INSERT INTO public.prices_file_col(prfc_prices_file_id, prfc_brand,  prfc_article, prfc_price, prfc_quality) VALUES (%s, %s, %s, %s, %s)")
		dataClear = (data['prfc_prices_file_id'], data['prfc_brand'], data['prfc_article'], data['prfc_price'], data['prfc_quality'])
		log.print_r(dataClear)
		self.cursor.execute(query, dataClear)
		self.conn.commit()
		return True

	# функция проверяет являетьс яли строка числом
	def is_number(self,s):
		if(s.isdigit()):
			return True
		else:
			try:
				float(s)
				return True
			except ValueError:
				return False

	# функция закрывает соединение с БД
	def closeWrite(self):
		# меняем статус загрузки
		#endtime = str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
		query = "UPDATE public.prices_file SET status = 1 WHERE prf_id = " + str(self.prf_id)
		log.print_r(query)
		log.print_r('Закончил загрузку файла в базу ' + config.get("pgconfig", "dbname"))
		self.cursor.execute(query)
		self.conn.commit()
		# обновляем счетчики прайсов
		countSQL = "UPDATE public.prices_file SET prf_count=(SELECT count(prfc_id)  FROM public.prices_file_col where prfc_prices_file_id = prf_id)"
		self.cursor.execute(countSQL)
		self.conn.commit()

		self.cursor.close()
		self.conn.close()
		log.print_r('Закрыл соединение с ' + config.get("pgconfig", "dbname"))
