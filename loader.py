import log
import os
import config
import psycopg2

# получаем настройки приложения
config = config.getConfig()

class Loader:

	# конструктор
	def __init__(self, war_id, sup_id):
		self.war_id= war_id
		self.sup_id = sup_id

	# функция ищет бренд, артикул, очищает остатки, цены и записывает новые
	def writerests(self, data):
		conn = psycopg2.connect(dbname=config.get("pgconfig","dbname"), user=config.get("pgconfig","user"),password=config.get("pgconfig","password"), host=config.get("pgconfig","host"))
		cursor = conn.cursor()
		
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