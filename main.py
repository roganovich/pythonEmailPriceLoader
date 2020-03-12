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
from parsers.shatem import Shateekat
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
from parsers.avtosputnik import Avtosputnik
from parsers.profitliga import PFLKrasnodar
from parsers.profitliga import PFLRostov
from parsers.toyotanova import Toyotanova
from parsers.voltag import Voltag
from parsers.jtc import Jtc


# получаем настройки приложения
config = config.getConfig()

# определяем каким парсером обрабатывать данные из письмо
def checkParser(email):
    if "ABS-AUTO" in email['email_subject']:
        return Absparser()
    if "pricekrd@auto-ray.com" in email['email_from']:
        return Autorayparser()
    if "ae@autoeuro.ru" in email['email_from']:
        return Autoeuro()
    if "no-reply@fokus-auto.com" in email['email_from']:
        return Focusauto()
    if "prices_export@shate-m.com" in email['email_from']:
        if "Склад Подольск" in email['email_subject']:
            return Shatepodolsk()
        if "Склад Минск" in email['email_subject']:
            return Shateminsk()
        if "Склад Екатеринбург" in email['email_subject']:
            return Shateekat()
    if "avtopartner99@bk.ru" in email['email_from']:
        return Autopartner()
    if "Остатки Kyariz" in email['email_subject']:
        return Kyariz()
    if "Прайс-лист ВАРИАНТ" in email['email_subject']:
        return Variant()
    if "post@mx.forum-auto.ru" in email['email_from']:
        return ForumAuto()
    if "vivatavtos@mail.ru" in email['email_from']:
        return Vivat()
    if "paliyauto@mail.ru" in email['email_from']:
        return Paliyauto()
    if "a.sergeev@autoluks.com" in email['email_from']:
        return Autolux()
    if "shop1.formula82@yandex.ru" in email['email_from']:
        return Formula82()
    if "krym_price@mail2.tpm.ru" in email['email_from']:
        return Tisrostov()
    if "noreply@tstarter.ru" in email['email_from']:
        return Transstarter()
    if "script@autoopt.ru" in email['email_from']:
        return Autoalians()
    if "price@variantauto.com" in email['email_from']:
        return Variant()
    if "seatrade-2012@mail.ru" in email['email_from']:
        return Satrade()
    if "Avtosputnik" in email['email_subject']:
        return Avtosputnik()
    if "Прайс вольтаж" in email['email_subject']:
        return Voltag()
    #if("robot@pr-lg.ru" in email['email_from']):
    if "ПрофитЛига склад Краснодар" in email['email_subject']:
        return PFLKrasnodar()
    if "ПрофитЛига склад Ростов" in email['email_subject']:
        return PFLRostov()
    if "optprice@ats-auto.ru" in email['email_from']:
        return Toyotanova()
    if "прайс JTC" in email['email_subject']:
        return Jtc()
    if("price@armtek.ru" in email['email_from']):
        if "Moscow" in email['email_subject']:
            return ArmtekMoscow()
        if "Krasnodar" in email['email_subject']:
            return ArmtekKrasnodar()
    if "vwadmin_sev@vwcrimea.ru" in email['email_from']:
        if "Севастополь" in email['email_subject']:
            return VwSevastopol()
    if "vwparts@vw-avtoholding.ru" in email['email_from']:
        if "Симферополь" in email['email_subject']:
            return VwSimferopol()

# profiler позволяет посчитать время выполнения процедуры внутри него
with profiler.Profiler() as p:
    # получаем все письма и данные в виде списка
    mLoader = MailLoader()
    emails = mLoader.getemails()
    if(not emails):
        log.print_r('Нет новыйх писем')
        exit()
    for email in emails:
        log.print_r('Нашел письмо "' + email['email_subject'] + '"')
        obj = checkParser(email)
        obj.email = email
        if (obj.needToLoad() == False):
            # удаляем письмо
            #mLoader.deleteEmail(email);
            log.print_r('Этот прайс уже загружали сегодня')
            continue
        # скачивания файла
        # получаем файлы вложенные в письмо
        files = mLoader.downloadAttachment(email['email_message'], obj)
        # загружаем файл в базу
        obj.upload()
        exit()
        # грузим только 1 письмо. т.к время соединения с базой заканчиваеться
        # удаляем письма помеченные флагом Deleted
        mLoader.connect.expunge()
        # закрываем соединение
        mLoader.connect.close()
        mLoader.connect.logout()
        # возвращаем массив данных
        exit()



