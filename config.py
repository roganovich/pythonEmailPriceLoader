import configparser
import os
# путь к фалу настроек
path = "settings.ini"

# функция создает базовый файл настроек
def createConfig():
    config = configparser.ConfigParser()
    config.add_section("email")
    config.set("email", "server", "127.0.0.1")
    config.set("email", "user", "root")
    config.set("email", "password", "root")
    config.add_section("system")
    config.set("system", "print", "1")
    # записываем в файл
    with open(path, "w") as config_file:
        config.write(config_file)


def getConfig():
    # проверяем существует ли фал настроек
    if os.path.exists(path):
        config = configparser.ConfigParser()
        config.read(path)
        if (config.get("system", "print") == "1"):
            print('Файл ' + path + ' существует')
    else:
        createConfig(path)
        config = configparser.ConfigParser()
        config.read(path)
        if (config.get("system", "print") == "1"):
            print('Файл ' + path + ' будет создан')
    return config
