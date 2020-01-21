# author Roganovich.R.M.
# work width email
import imaplib
import email
import base64
import log
import os
import config

# получаем настройки приложения
config = config.getConfig()

# функция подключения к почтовому ящику по imaplib
def auth(server, username, password):
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
def hascyrillic(s):
    #=?utf-8?B?0YLQtdGB0YI=?=
    return True if "?utf-8?B?" in s else False

# функция декодирует base64 в кирилицу
def translit(s):
    # обрезаем лишние символы
    subjectutf8 = s[10:-2]
    email_subject = base64.b64decode(subjectutf8)
    # переводит тему в русский язык
    ru_subject = str(email_subject,'utf-8')
    return ru_subject

# скачивания файла
def downloadAttachment(email):
    files = []
    # путь к сохранения файла
    path = config.get("email", "attachmentFolder")
    # есть ли вложения в письме
    if email.is_multipart():
        for part in email.walk():
            content_type = part.get_content_type()
            filename = part.get_filename()
            # проверяем на наличие имени у файла
            if filename:
                filePath = path + "/" + part.get_filename()
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
def getemail():
    # будем возвращать массив данных
    returnData = []
        # настройки подключения
    server = config.get("email", "server")
    user = config.get("email", "user")
    password = config.get("email", "password")
    mail = auth(server, user, password)
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
                if(hascyrillic(email_subject)):
                    email_subject = translit(email_subject)
                # журнал
                log.print_r('Нашел письмо ' + email_subject + ' от ' + email_from)
                # скачивания файла
                files = downloadAttachment(email_message)
                # заполняем массив данных
                returnData.append({'msg_id':email_msg_id, 'email_date':email_date, 'subject':email_subject, 'files':files})
            # перемещаем отработанные письма
            copy_res = mail.copy(uid, 'Completed')
            if copy_res[0] == 'OK':
                mail.store(uid, '+FLAGS', '\\Deleted')
            log.print_r('Удаляем письмо ' + email_subject + ' от ' + email_from)
    # закрываем соединение
    mail.close()
    mail.logout()
    # возвращаем массив данных
    return returnData
