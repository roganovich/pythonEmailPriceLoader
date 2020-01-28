# author Roganovich.R.M.
# work width email
import imaplib
import email
import base64
import log
import os
import config
from parsers.abs import Absparser
from parsers.autoray import Autorayparser

# получаем настройки приложения
config = config.getConfig()

class MailLoader():
    # функция удаляет письмо из каталога
    def deleteEmail(self, mail, uid, email_subject, email_from):
        # перемещаем отработанные письма
        copy_res = mail.copy(uid, 'Completed')
        if copy_res[0] == 'OK':
            mail.store(uid, '+FLAGS', '\\Deleted')
        log.print_r('Удаляем письмо ' + email_subject + ' от ' + email_from)

    # проверка. нужно ли грузить это письмо. ищем каталог результата в котором учитываетьс дата, склад, поставщик
    def needToLoad(self, mail_subject,email_from):
        if "ABS-AUTO" in mail_subject:
            obj = Absparser()
            if os.path.exists(obj.defGetResultFolder()):
                return False
        if "pricekrd@auto-ray.com" in email_from:
            obj = Autorayparser()
            if os.path.exists(obj.defGetResultFolder()):
                return False
        return True

    # получаем названия парсера, она же папка для регультата
    def getParserPath(self, mail_subject,email_from):
        if "ABS-AUTO" in mail_subject:
            obj = Absparser()
            # очистка мусора из каталога
            obj.clearDir()
            return obj.filePathExtract
        if "pricekrd@auto-ray.com" in email_from:
            obj = Autorayparser()
            # очистка мусора из каталога
            obj.clearDir()
            return obj.filePathExtract

    # функция подключения к почтовому ящику по imaplib
    def auth(self, server, username, password):
        # журнал
        log.print_r('Подключаюсь к ' + server)
        imap = imaplib.IMAP4_SSL(server)
        try:
            imap.login(str(username), str(password))
            # журнал
            log.print_r("Успешно подключились к " + username)
            return imap
        except:
            # журнал
            log.print_r("Не удалось подключиться к " + username)

    # функция проверяет строку на кодировку base64(ей кодируют кирилицу)
    def hascyrillic(self, s):
        #=?utf-8?B?0YLQtdGB0YI=?=
        return True if "?utf-8?B?" in s else False

    # функция декодирует base64 в кирилицу
    def translit(self, s):
        alpha = '=?utf-8?B'
        bravo = '?='
        startpos = s.find(alpha) + len(alpha)
        endpos = s.find(bravo, startpos)
        cirilic = s[startpos:endpos]
        # обрезаем лишние символы
        #subjectutf8 = s[10:-2]
        ru_text_base = base64.b64decode(cirilic)
        # переводит тему в русский язык
        ru_text = str(ru_text_base,'utf-8')
        return ru_text

    # скачивания файла
    def downloadAttachment(self, email, path):
        files = []
        # есть ли вложения в письме
        if email.is_multipart():
            for part in email.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                filename = part.get_filename()
                if (self.hascyrillic(filename)):
                    filename = self.translit(filename)
                # проверяем на наличие имени у файла
                if filename:
                    # путь к сохранения файла
                    filePath = path + "/" + filename
                    # если этот файл уже есть удалить
                    if os.path.exists(filePath):
                        log.print_r('Удаляем ' + filePath)
                        os.remove(filePath)
                    # открываем файл для записи
                    with open(filePath, 'wb') as new_file:
                        # сохраняем файл в папку для дальнейшей загрузки
                        new_file.write(part.get_payload(decode=True))
                        log.print_r('Нашел файл. Сохраняем ' + filePath)
                        # добавляем путь к файлу в массив с данными
                        files.append(filePath)
        if (not  files):
            log.print_r('Нет файлов для скачивания')
        # возвращаем массив с новыми файлами
        return files

    # выполняем подключение
    def getemail(self):
        # будем возвращать массив данных
        returnData = []
            # настройки подключения
        server = config.get("email", "server")
        user = config.get("email", "user")
        password = config.get("email", "password")
        mail = self.auth(server, user, password)
        # получаем список каталогов
        mail.list()
        # выбираем входящие
        mail.select("Prices")
        # Получаем массив со списком найденных почтовых сообщений
        result, data = mail.search(None, "ALL")
        # Сохраняем в переменную ids строку с номерами писем
        mail_ids = data[0]
        # Получаем массив номеров писем
        id_list = mail_ids.split()
        # кол-во писем в ящике
        mail_coun = len(id_list)
        # если нет новых писем возвращаем пустой массив
        if(mail_coun == 0):
            return returnData
        # Задаем переменную latest_email_id, значением которой будет номер первого письма
        first_email_id = id_list[0]
        # Задаем переменную latest_email_id, значением которой будет номер последнего письма
        latest_email_id = id_list[-1]
        # Получаем письмо с идентификатором latest_email_id (последнее письмо).
        result, data = mail.fetch(latest_email_id, "(RFC822)")
        # В переменную raw_email заносим необработанное письмо
        raw_email = data[0][1]
        # Переводим текст письма в кодировку UTF-8 и сохраняем в переменную raw_email_string
        raw_email_string = raw_email.decode('UTF-8')
        # Получаем заголовки и тело письма и заносим результат в переменную email_message.
        email_message = email.message_from_string(raw_email_string)
        # кому отправлено письмо
        email_to = email_message['To']
        # от кого отправлено письмо
        email_from = email.utils.parseaddr(email_message['From'])
        # дата отправки письма
        email_date = email_message['Date']
        # тема письма
        email_subject = email_message['Subject']
        # идентификатор письма
        email_msg_id = email_message['Message-Id']
        # перебор всех писем
        for uid in id_list:
            # need str(i)
            result, data = mail.fetch(uid, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    email_message = email.message_from_bytes(response_part[1])
                    # кому отправлено письмо
                    email_to = email_message['To']
                    # от кого отправлено письмо  #email.utils.parseaddr
                    email_from = email_message['From']
                    # дата отправки письма
                    email_date = email_message['Date']
                    # тема письма
                    email_subject = email_message['Subject']
                    # идентификатор письма
                    email_msg_id = email_message['Message-Id']
                    # проверяем кирилицу
                    if(self.hascyrillic(email_subject)):
                        email_subject = self.translit(email_subject)
                    if (self.hascyrillic(email_from)):
                        email_from = self.translit(email_from)
                    # журнал
                    log.print_r('Нашел письмо ' + email_subject + ' от ' + email_from)
                    if(self.needToLoad(email_subject,email_from) == False):
                        # удаляем письмо
                        self.deleteEmail(mail, uid, email_subject, email_from);
                        log.print_r('Этот прайс уже загружали сегодня')
                        continue
                    # скачивания файла
                    #получаем путь сохранения файла из письма
                    path = self.getParserPath(email_subject,email_from)
                    # получаем файлы вложенные в письмо
                    files = self.downloadAttachment(email_message,path)
                    # заполняем массив данных
                    returnData.append({'msg_id':email_msg_id, 'email_date':email_date, 'subject':email_subject, 'email_from': email_from, 'files':files})
                    # удаляем письмо
                    self.deleteEmail(mail, uid, email_subject, email_from);

        # удаляем письма помеченные флагом Deleted
        mail.expunge()
        # закрываем соединение
        mail.close()
        mail.logout()
        # возвращаем массив данных
        return returnData

