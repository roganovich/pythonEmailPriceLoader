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
    # загружаем файлы в базу
    for warhouse_id in model.pricesFiles:
        model.workWidthFiles(warhouse_id)


    exit()



