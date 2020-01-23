import sys
import profiler
import mail
import config
import log
from parsers.abs import Absparser
# получаем настройки приложения
config = config.getConfig()

def checkParser(email):
    # eсли есть вроженый файл
    if(email['files']):
        if "ABS-AUTO" in email['subject']:
            obj = Absparser()
            obj.data = email
            obj.upload()
            exit()


# profiler позволяет посчитать время выполнения процедуры внутри него
with profiler.Profiler() as p:
    # получаем все письма и данные в виде списка
    emails = mail.getemail()
    if(not emails):
        log.print_r('Нет новыйх писем')
        exit()
    # print(emails)
    for email in emails:
        checkParser(email)



