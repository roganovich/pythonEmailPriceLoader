import profiler
import config
import log

from parsers.major import Major
# получаем настройки приложения
config = config.getConfig()

# profiler позволяет посчитать время выполнения процедуры внутри него
with profiler.Profiler() as p:
    log.print_r("Начал работу с Major")
    priceModel =  Major()
    # скачиваем все прайсы
    priceModel.downloadFiles()
    priceModel.workWidthFiles()
    exit()



