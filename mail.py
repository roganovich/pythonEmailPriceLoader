#work width email
#author Roganovich.R.M.

import imaplib
import email
import base64
import sys
# настройки подключения

# функция подключения к почтовому ящику по imaplib
def auth(username, password):
    imap = imaplib.IMAP4_SSL(server)
    try:
        imap.login(str(username), str(password))
        print("Вошли!")
        return imap
    except:
        print("Не удалось войти")

def hascyrillic(s):
    #=?utf-8?B?0YLQtdGB0YI=?=
    return True if "?utf-8?B?" in s else False

def translit(s):
    # переводит тему в русский язык
    subjectutf8 = s[10:-2]
    email_subject = base64.b64decode(subjectutf8)
    ru_subject = str(email_subject,'utf-8')
    return ru_subject

# выполняем подключение
mail = auth(user, password)

mail.list()
mail.select("inbox")

# Получаем массив со списком найденных почтовых сообщений
result, data = mail.search(None, "ALL")
# Сохраняем в переменную ids строку с номерами писем
mail_ids = data[0]
# Получаем массив номеров писем
id_list = mail_ids.split()
# кол-во писем в ящике
mail_coun = len(id_list)
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
for id in id_list:
    # need str(i)
    result, data = mail.fetch(id, '(RFC822)')
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

            print(email_subject)
            # работа с вложениями
            for part in email_message.walk():
                # print(part.as_string() + "\n")
                # пропускаем мусор
                if part.get_content_maintype() == 'multipart': continue
                if part.get_content_maintype() == 'text': continue
                if part.get('Content-Disposition') == 'inline': continue
                if part.get('Content-Disposition') is None: continue

                filename = part.get_filename()
                print(filename)
mail.close()
mail.logout()