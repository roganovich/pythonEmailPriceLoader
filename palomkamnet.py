import profiler
import config
import log

from parsers.mikado import Mikado
# получаем настройки приложения
config = config.getConfig()

# profiler позволяет посчитать время выполнения процедуры внутри него
with profiler.Profiler() as p:

    model = Mikado()
    # скачиваем все прайсы
    model.downloadFiles()
    model.workWidthFiles()


    exit()



