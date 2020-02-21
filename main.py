import sys
import profiler

import config
import log
from mail import MailLoader

from parsers.abs import Absparser
from parsers.autoray import Autorayparser
from parsers.autoeuro import Autoeuro
from parsers.focusauto import Focusauto
from parsers.shatem import Shatepodolsk
from parsers.shatem import Shateminsk
from parsers.autopartner import Autopartner
from parsers.kyariz import Kyariz
from parsers.variant import Variant
from parsers.armtek import ArmtekMoscow
from parsers.armtek import ArmtekKrasnodar
from parsers.vivat import Vivat
from parsers.forumauto import ForumAuto
from parsers.paliyauto import Paliyauto
from parsers.autolux import Autolux
from parsers.formula82 import Formula82
from parsers.tisrostov import Tisrostov
from parsers.transstarter import Transstarter
from parsers.vwsevastopol import VwSevastopol
from parsers.vwsevastopol import VwSimferopol
from parsers.autoalians import Autoalians
from parsers.seatrade import Satrade


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
    if "shop1.formula82@yandex.ru" in email['email_from']:
        return Formula82(email)
    if "krym_price@mail2.tpm.ru" in email['email_from']:
        return Tisrostov(email)
    if "noreply@tstarter.ru" in email['email_from']:
        return Transstarter(email)
    if "script@autoopt.ru" in email['email_from']:
        return Autoalians(email)
    if "price@variantauto.com" in email['email_from']:
        return Variant(email)
    if "seatrade-2012@mail.ru" in email['email_from']:
        return Satrade(email)
    if("price@armtek.ru" in email['email_from']):
        if "Moscow" in email['email_subject']:
            return ArmtekMoscow(email)
        if "Krasnodar" in email['email_subject']:
            return ArmtekKrasnodar(email)
    if "vwadmin_sev@vwcrimea.ru" in email['email_from']:
        if "Севастополь" in email['email_subject']:
            return VwSevastopol(email)
    if "vwparts@vw-avtoholding.ru" in email['email_from']:
        if "Симферополь" in email['email_subject']:
            return VwSimferopol(email)

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



