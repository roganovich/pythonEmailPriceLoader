import sys
import profiler

import config
import log
from mail import MailLoader

from parsers.abs import Absparser
from parsers.autoray import Autorayparser
from parsers.autoeuro import Autoeuro
from parsers.focusauto import Focusauto
from parsers.shatepodolk import Shatepodolsk
from parsers.shateminsk import Shateminsk


# получаем настройки приложения
config = config.getConfig()

# определяем каким парсером обрабатывать данные из письмо
def checkParser(email):
    if "ABS-AUTO" in email['email_subject']:
        return Absparser(email)
    if "pricekrd@auto-ray.com" in email['email_from']:
        return Autorayparser(email)
    if "ae@autoeuro.ru" in email['email_from']:
        return Autoeuro(email)
    if "no-reply@fokus-auto.com" in email['email_from']:
        return Focusauto(email)
    if "prices_export@shate-m.com" in email['email_from']:
        if "Склад Подольск" in email['email_subject']:
            return Shatepodolsk(email)
        if "Склад Минск" in email['email_subject']:
            return Shateminsk(email)

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
        # удаляем письмо
        #mLoader.deleteEmail(email);
        # загружаем файл в базу
        obj.upload()
    # удаляем письма помеченные флагом Deleted
    mLoader.connect.expunge()
    # закрываем соединение
    mLoader.connect.close()
    mLoader.connect.logout()
    # возвращаем массив данных



