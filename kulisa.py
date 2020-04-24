import profiler
import config
import log
from parsers.kulisa import Kulisa
# получаем настройки приложения
config = config.getConfig()

# profiler позволяет посчитать время выполнения процедуры внутри него
with profiler.Profiler() as p:
    model = Kulisa()
    # скачиваем все прайсы
    model.downloadFiles()
    model.upload()
    exit()



