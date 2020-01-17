import profiler
import config
import mail
# путь к фалу настроек
path = "settings.ini"


with profiler.Profiler() as p:
    config = config.getConfig(path)
    mail.getemail(config)