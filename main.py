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

from parsers.autopartner import Autopartner
from parsers.kyariz import Kyariz
from parsers.variant import Variant
from parsers.armtekmoscow import ArmtekMoscow
from parsers.armtekkrasnodar import ArmtekKrasnodar
from parsers.vivat import Vivat
from parsers.forumauto import ForumAuto
from parsers.paliyauto import Paliyauto
from parsers.autolux import Autolux

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
    if "Авто-Партнер" in email['email_subject']:
        return Autopartner(email)
    if "Остатки Kyariz" in email['email_subject']:
        return Kyariz(email)
    if "Прайс-лист ВАРИАНТ" in email['email_subject']:
        return Variant(email)
    if "post@mx.forum-auto.ru" in email['email_from']:
        return ForumAuto(email)
    if "vivatavtos@mail.ru" in email['email_from']:
        return Vivat(email)
    if "paliyauto@mail.ru" in email['email_from']:
        return Paliyauto(email)
    if "a.sergeev@autoluks.com" in email['email_from']:
        return Autolux(email)
    if "price@armtek.ru" in email['email_from']:
        if "Ostatki_Moscow" in email['email_subject']:
            return ArmtekMoscow(email)
        if "Ostatki_Krasnodar" in email['email_subject']:
            return ArmtekKrasnodar(email)

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
        # загружаем файл в базу
        obj.upload()
        # грузим только 1 письмо. т.к время соединения с базой заканчиваеться
        # удаляем письма помеченные флагом Deleted
        mLoader.connect.expunge()
        # закрываем соединение
        mLoader.connect.close()
        mLoader.connect.logout()
        # возвращаем массив данных
        exit()



