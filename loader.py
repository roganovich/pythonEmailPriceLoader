import log
import os
import config
import datetime
import csv
import psycopg2

# получаем настройки приложения
config = config.getConfig()

class Loader:
	# конструктор
	def __init__(self, war_id, sup_id):
		self.war_id= war_id
		self.sup_id = sup_id

		dateCreate = str(datetime.datetime.today().strftime("%Y%m%d"))
		resultPath = config.get("email","resultsFolder") + '/' + dateCreate + '/' + self.sup_id + '/' + self.war_id + '/'
		self.file_path = os.path.join(self.basePath, resultPath)
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

	# функция ищет бренд, артикул, очищает остатки, цены и записывает новые
	def writerests(self, data):
		conn = psycopg2.connect(dbname=config.get("pgconfig","dbname"), user=config.get("pgconfig","user"),password=config.get("pgconfig","password"), host=config.get("pgconfig","host"))
		cursor = conn.cursor()
		print(data)
		exit()
		columns = {}
		cursor.execute("INSERT INTO public.parsertask(pt_date_start, pt_date_end, pt_param, pt_status, pt_src_id, pt_tmpfile, pt_table, pt_brand) VALUES (%S, %S, %S, %S, %S, %S, %S, %S, %S)", (columns))

		# ищем бренд
		find_brand_sql = "SELECT * FROM brands WHERE bra_name = '" + data[1] + "'"
		print(find_brand_sql)
		cursor.execute(find_brand_sql)
		brand = cursor.fetchone()
		bra_id = str(brand[0])
		#print(brand)
		# ищем артикул
		find_article_sql = "SELECT * FROM articles WHERE art_bra_id = "+ bra_id +" AND art_article = '" + data[0] + "'"
		print(find_article_sql)
		cursor.execute(find_article_sql)
		article = cursor.fetchone()
		if(not article):
			print('Не нашел '+ data[0] + ' '+ data[1])
			exit()
		art_id = str(article[0])
		print(article)
		#удаляем цены
		delete_rests_sql = "DELETE * FROM prices WHERE prc_art_id = "+ art_id +" AND prc_sup_id = " + self.war_id
		print(delete_rests_sql)


		#удаляем остатки
		delete_prices_sql = "DELETE FROM rests WHERE  rst_art_id = "+ art_id +" AND rst_war_id = " + self.sup_id
		print(delete_rests_sql)
		
		conn.commit()
		cursor.close()
		conn.close()
		
		exit()