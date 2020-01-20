import sys
import profiler
import mail
import config
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
    # print(emails)
    for email in emails:
        checkParser(email)



