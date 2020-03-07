# author Roganovich.R.M.
# work width email
import imaplib
import email
import base64
import quopri
import log
import os
import re
import config

# получаем настройки приложения
config = config.getConfig()

class MailLoader():


    def __init__(self):
        # корневая директория
        self.dirname = os.path.dirname(__file__)
        # настройки подключения
        server = config.get("email", "server")
        user = config.get("email", "user")
        password = config.get("email", "password")
        self.connect = self.auth(server, user, password)


    # функция удаляет письмо из каталога
    def deleteEmail(self, email):
        uid = email['uid']
        email_subject = email['email_subject']
        email_from = email['email_from']
        # перемещаем отработанные письма
        copy_res = self.connect.copy(uid, 'Completed')
        if copy_res[0] == 'OK':
            self.connect.store(uid, '+FLAGS', '\\Deleted')
        else:
            log.print_r('Не удалось скопировать "' + email_subject + '"')
        log.print_r('Удаляем письмо "' + email_subject + '"')
        # удаляем письма помеченные флагом Deleted
        self.connect.expunge()

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
            exit()

    # функция проверяет строку на кодировку base64(ей кодируют кирилицу)
    def hascyrillic(self, s):
        return True if "=?" in s else False

    # функция декодирует base64 в кирилицу
    def translit(self, s):
        if "=?utf-8?B?" in s:
            alpha = '=?utf-8?B?'
            char = 'utf-8'
            type = 'base64'
        elif "=?UTF-8?B?" in s:
            alpha = '=?UTF-8?B?'
            char = 'utf-8'
            type = 'base64'
        elif "=?windows-1251?b?" in s:
            alpha = '=?windows-1251?B?'
            char = 'windows-1251'
            type = 'base64'
        elif "=?windows-1251?B?" in s:
            alpha = '=?windows-1251?B?'
            char = 'windows-1251'
            type = 'base64'
        elif "=?Windows-1251?Q?" in s:
            alpha = '=?Windows-1251?Q?'
            char = 'windows-1251'
            type = 'quopri'
            s = s.replace('_', ' ')
        elif "=?windows-1251?Q?" in s:
            alpha = '=?windows-1251?Q?'
            char = 'windows-1251'
            type = 'quopri'
            s = s.replace('_', ' ')
        elif "=?WINDOWS-1251?B?" in s:
            alpha = '=?WINDOWS-1251?B?'
            char = 'windows-1251'
            type = 'base64'
        elif "=?WINDOWS-1251?Q?" in s:
            alpha = '=?windows-1251?Q?'
            char = 'windows-1251'
            type = 'quopri'
            s = s.replace('_', ' ')
        bravo = '?='

        # обрезаем лишние символы
        cirilic = s.replace("\r","").replace("\n","").replace(alpha, '').replace(bravo, '')

        if (type == 'base64'):
            ru_text_base = base64.b64decode(cirilic)
        if (type == 'quopri'):
            ru_text_base = quopri.decodestring(cirilic)
        # переводит тему в русский язык
        ru_text = str(ru_text_base, char)

        return ru_text

    # скачивания файла
    def downloadAttachment(self, email, obj):
        # получаем путь сохранения файла из письма
        path = obj.getParserPath()
        files = []
        # есть ли вложения в письме
        if email.is_multipart():
            for part in email.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                filename = part.get_filename()
                # проверяем на наличие имени у файла
                if filename:

                    clearName = ""
                    # разбиваем тему на абзацы
                    filenameRows = filename.split('\n')
                    if (len(filenameRows) > 1):
                        for name in filenameRows:
                            if (self.hascyrillic(name)):
                                try:
                                    clearName += self.translit(name)
                                except:
                                    clearName = ""
                            else:
                                clearName += name
                    else:
                        if (self.hascyrillic(filename)):
                            try:
                                clearName += self.translit(filename)
                            except:
                                clearName = filename
                        else:
                            clearName = filename

                    # очищаем имя файла от мусора
                    clearName = re.sub(r'[^0-9A-Za-zа-яА-ЯёЁ\s+\/\.\-\\]+', r'', clearName.strip())
                    # если не удалось получить имя файла, то делаем его базовым
                    if (not clearName):
                        clearName = "price." + obj.filetype
                    filePath = path + clearName
                    # если этот файл уже есть удалить
                    if os.path.exists(filePath):
                        log.print_r('Удаляем старый файл ' + filePath)
                        os.remove(filePath)
                    # открываем файл для записи
                    new_file = open(filePath, 'wb')
                    # сохраняем файл в папку для дальнейшей загрузки

                    try:
                        os.chmod(filePath, 0o600)
                        new_file.write(part.get_payload(decode=True))
                        log.print_r('Нашел файл '+clearName+'. Сохраняем в ' + filePath)
                        # добавляем путь к файлу в массив с данными
                        files.append(filePath)
                    except:
                        log.print_r('Нашел файл '+clearName+'. Не смог скопировать в ' + filePath)
                    # закрытие файла
                    new_file.close()

        if (not  files):
            log.print_r('Нет файлов для скачивания')
        # возвращаем массив с новыми файлами
        return files

    # выполняем подключение
    def getemails(self):
        # будем возвращать массив данных
        returnData = []

        # получаем список каталогов
        self.connect.list()
        # выбираем входящие
        self.connect.select("Prices")
        # Получаем массив со списком найденных почтовых сообщений
        result, data = self.connect.search(None, "ALL")
        # Сохраняем в переменную ids строку с номерами писем
        mail_ids = data[0]
        # Получаем массив номеров писем
        id_list = mail_ids.split()
        # кол-во писем в ящике
        mail_coun = len(id_list)

        # если нет новых писем возвращаем пустой массив
        if(mail_coun == 0):
            return returnData
        # перебор всех писем
        for uid in id_list:
            result, data = self.connect.fetch(uid, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    email_message = email.message_from_bytes(response_part[1])

                    # кому отправлено письмо
                    email_to = str(email_message['To'])
                    # от кого отправлено письмо  #email.utils.parseaddr
                    email_from = str(email_message['From'])
                    # дата отправки письма
                    email_date = str(email_message['Date'])
                    # тема письма
                    email_subject_data = str(email_message['Subject'])
                    # идентификатор письма
                    email_msg_id = str(email_message['Message-Id'])

                    email_subject = ""
                    # разбиваем тему на абзацы
                    subjectsRows = email_subject_data.split('\n')
                    if(len(subjectsRows)>1):
                        for subj in subjectsRows:
                            if (self.hascyrillic(subj)):
                                email_subject += self.translit(subj)
                            else:
                                email_subject += subj
                    else:
                        # проверяем кирилицу
                        if (self.hascyrillic(email_subject_data)):
                            email_subject = self.translit(email_subject_data)
                        else:
                            email_subject = email_subject_data
                    if(not email_subject):
                        log.print_r('Плохое письмо: нет email_subject')
                        continue
                    if (not email_from):
                        log.print_r('Плохое письмо: нет email_from')
                        continue
                    #разбиваем адресата на имя и адрес ящика
                    email_from_data = email_from.split('<')
                    if (len(email_from_data)>1):
                        email_from = email_from_data[1].replace('<', '').replace('>', '')
                    else:
                        email_from = email_from

                    returnData.append({'uid':uid,'msg_id': email_msg_id, 'email_date': email_date, 'email_subject': email_subject,
                                       'email_from': email_from, 'email_message':email_message})

        return returnData

