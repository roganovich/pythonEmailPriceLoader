# author Roganovich.R.M.
import config
# получаем настройки приложения
config = config.getConfig()

def print_r(str):
    if (config.get("system", "print") == "1"):
        print(str)