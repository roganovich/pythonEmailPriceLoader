# author Roganovich.R.M.
import config
import datetime
# получаем настройки приложения
config = config.getConfig()

def print_r(str):
    if (config.get("system", "print") == "1"):
        today = datetime.datetime.today()
        print(today.strftime("%Y-%m-%d %H:%M:%S") + " " + str)