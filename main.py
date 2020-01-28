import sys
import profiler

import config
import log
from parsers.abs import Absparser
from parsers.autoray import Autorayparser
from mail import MailLoader
# получаем настройки приложения
config = config.getConfig()

# определяем каким парсером обрабатывать данные из письмо
def checkParser(email):
    # eсли есть вроженый файл
    if(email['files']):
        if "ABS-AUTO" in email['subject']:
            log.print_r('Запускаю Abs')
            obj = Absparser()
            obj.data = email
            obj.upload()
            log.print_r('Закончили работу с ' + obj.name)
        if "pricekrd@auto-ray.com" in email['email_from']:
            log.print_r('Запускаю Autoray')
            obj = Autorayparser()
            obj.data = email
            obj.upload()
            log.print_r('Закончили работу с ' + obj.name)


# profiler позволяет посчитать время выполнения процедуры внутри него
with profiler.Profiler() as p:
    # получаем все письма и данные в виде списка
    obj = MailLoader()
    emails = obj.getemail()
    if(not emails):
        log.print_r('Нет новыйх писем')
        exit()
    for email in emails:
        checkParser(email)



