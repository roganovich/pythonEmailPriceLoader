import sys
import profiler

import config
import log
from mail import MailLoader

from parsers.abs import Absparser
from parsers.autoray import Autorayparser
from parsers.autoeuro import Autoeuro

# получаем настройки приложения
config = config.getConfig()

# определяем каким парсером обрабатывать данные из письмо
def checkParser(email):
    if "ABS-AUTO" in email['email_subject']:
        return Absparser()
    if "pricekrd@auto-ray.com" in email['email_from']:
        return Autorayparser()
    if "ae@autoeuro.ru" in email['email_from']:
        return  Autoeuro()

# profiler позволяет посчитать время выполнения процедуры внутри него
with profiler.Profiler() as p:
    # получаем все письма и данные в виде списка
    mLoader = MailLoader()
    emails = mLoader.getemails()
    if(not emails):
        log.print_r('Нет новыйх писем')
        exit()
    for email in emails:
        obj = checkParser(email)
        if (obj.needToLoad() == False):
            # удаляем письмо
            mLoader.deleteEmail(email);
            log.print_r('Этот прайс уже загружали сегодня')
            continue
        # скачивания файла
        # получаем путь сохранения файла из письма
        path = obj.getParserPath()
        # получаем файлы вложенные в письмо
        files = mLoader.downloadAttachment(email['email_message'], path)
        obj.upload()
        # удаляем письмо
        mLoader.deleteEmail(email);
    # удаляем письма помеченные флагом Deleted
    # mLoader.expunge()
    # закрываем соединение
    mLoader.connect.close()
    mLoader.connect.logout()
    # возвращаем массив данных



