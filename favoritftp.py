import profiler
import config
import log

from parsers.favorit import FavoritKRS
from parsers.favorit import Favorit
# получаем настройки приложения
config = config.getConfig()

# profiler позволяет посчитать время выполнения процедуры внутри него
with profiler.Profiler() as p:
    log.print_r("Начал работу с Favorit")
    favoritModel = Favorit()
    # скачиваем все прайсы
    favoritModel.downloadFiles()
    #favoritModel.workWidthFiles()

    log.print_r("Начал работу с FavoritKRS")
    favoritKRSModel = FavoritKRS()
    # скачиваем все прайсы
    favoritKRSModel.downloadFiles()
    #favoritKRSModel.workWidthFiles()
    exit()



