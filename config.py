import configparser
import os

# функция создает базовый фал настроек
def createConfig(path):
    config = configparser.ConfigParser()
    config.add_section("email")
    config.set("email", "server", "127.0.0.1")
    config.set("email", "user", "root")
    config.set("email", "password", "root")
    # записываем в файл
    with open(path, "w") as config_file:
        config.write(config_file)


def getConfig(path):
    # проверяем существует ли фал настроек
    if os.path.exists(path):
        print('Файл ' + path + ' существует')
        config = configparser.ConfigParser()
        config.read(path)
    else:
        print('Файл ' + path + ' будет создан')
        createConfig(path)
    return config
