import sys
import os
from json import load
from random import choice, randint, random
from threading import Thread
from time import sleep, strftime
from requests import get, post
from fake_useragent import UserAgent
ua = UserAgent().random 

def buy_slave(id):
    # Покупка раба
    post(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buySlave",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": ua,
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
        json={"slave_id": id},
    )

def buy_fetter(id):
    # Покупка оков
    post(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buyFetter",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": ua,
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
        json={"slave_id": id},
    )

def sell_slave(id):
    # Продажа раба
    post(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/saleSlave",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": ua,
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
        json={"slave_id": id},
    )

def job_slave(id):
    # Выдача работы
    post(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/jobSlave",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": ua,
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
        json={
            "slave_id": id,
            "name": choice(job),
        },
    )

def get_user(id):
    # Информация о пользователе
    return get(
        f"https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/user?id={id}",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": ua,
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
    ).json()


def get_slave_list(id):
    # Список рабов пользователя
    return get(
        f"https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/slaveList?id={id}",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": ua,
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
    ).json()

def get_top_users():
    # Вывод списка топ игроков
    return get(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/topUsers",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": ua,
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
    ).json()

def get_start():
    # Получение полной информации о своём профиле
    return get(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/start",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": ua,
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
    ).json()

def upgrade_slaves():
    # Прокачка рабов (1000 в минуту)
    while True:
        try:
            # Перебор списка рабов
            for slave in get_start()["slaves"]:
                balance = get_user(my_id)["balance"]
                if int(balance) >= 39214:
                    slave_price = get_user(slave["id"])["price"]
                    while int(slave_price) <= 26151:
                        sell_slave(slave["id"])
                        print(f"Продал id{slave['id']} для улучшения")
                        buy_slave(slave["id"])
                        print(f"Улучшил id{slave['id']}")
                        sleep(delay + random())
                        slave_price = get_user(slave["id"])["price"]
                    balance = get_user(my_id)["balance"]
        except Exception as e:
            print(e.args)
            sleep(delay + random())

def buy_top_users_slaves():
    #  Прекупка рабов у топ игроков
    while True:
        try:
            top_users = get_top_users()
            if "list" in top_users.keys():
                for top_user in top_users["list"]:
                    top_user_slaves = get_slave_list(int(top_user["id"]))
                    if "slaves" in top_user_slaves.keys():
                        for slave in top_user_slaves["slaves"]:
                            if int(slave["fetter_to"]) == 0:
                                slave_id = slave["id"]
                                slave_info = get_user(slave_id)
                                if slave_info["price"] <= max_price:
                                    # Покупка раба
                                    buy_slave(slave_id)
                                    
                                    # Получение информации о себе
                                    me = get_user(my_id)

                                    print(f"""\n===[{strftime("%d.%m.%Y %H:%M:%S")}]===""")
                                    print(f"""Купил id{slave_info["id"]} за {slave_info["price"]} у id{top_user["id"]}""")
                                    print(f"""Баланс: {me['balance']}""")
                                    print(f"""Рабов: {me['slaves_count']}""")
                                    print(f"""Доход в минуту: {me['slaves_profit_per_min']}""")
                                    print(f"""===========================""")

                                    # Покупает оковы только что купленному рабу
                                    if buy_fetters == 1:
                                        buy_fetter(slave_id)
                                        print(
                                            f"Купил оковы vk.com/id{slave_id}"
                                        )
                                    sleep(delay + random())
        except Exception as e:
            print(e.args)
            sleep(delay + random())

def buy_slaves():
    # Покупка рабов
    while True:
        try:
            # Случайный раб в промежутке
            slave_id = randint(1, 646959225)
            slave_info = get_user(slave_id)

            # Проверка раба на соотвествие настройкам цены
            while int(slave_info["price"]) >= max_price:
                slave_id = randint(1, 646959225)
                slave_info = get_user(slave_id)

            # Покупка раба
            buy_slave(slave_id)

            # Получение информации о себе
            me = get_user(my_id)
            
            print(f"""\n===[{strftime("%d.%m.%Y %H:%M:%S")}]===""")
            print(f"""Купил id{slave_info["id"]} за {slave_info["price"]}""")
            print(f"""Баланс: {me['balance']}""")
            print(f"""Рабов: {me['slaves_count']}""")
            print(f"""Доход в минуту: {me['slaves_profit_per_min']}""")
            print(f"""===========================\n""")

            # Покупка оков только что купленному рабу
            if buy_fetters == 1:
                buy_fetter(slave_id)
                print(f"Купил оковы vk.com/id{slave_id}")

            sleep(delay + random())
        except Exception as e:
            print(e.args)
            sleep(delay + random())

def buy_fetters():
    # Покупка оков
    while True:
        try:
            slaves = get_start()["slaves"]

            # Удаление первого раба из списка (чтобы не происходило коллизии с прокачкой)
            if conf_upgrade_slaves == 1:
                del slaves[0]

            # Перебор списка рабов
            for slave in slaves:
                # Проверка на наличие оков
                if int(slave["fetter_to"]) == 0:
                    buy_fetter(slave["id"])
                    me = get_user(my_id)
                    print(f"Купил оковы id{slave['id']}")
                    print(f"Баланс: {me['balance']}\n")
                    sleep(delay + random())
        except Exception as e:
            print(e.args)
            sleep(delay + random())

def job_slaves():
    # Выдача работы безработным
    while True:
        try:
            slaves = get_start()["slaves"]
            if conf_buy_slaves == 1:
                del slaves[0]
            # Перебор списка рабов
            for slave in slaves:
                # Проверка на наличие у раба работы
                if not slave["job"]["name"]:
                    job_slave(int(slave["id"]))
                    print(f"Дал работу id{slave['id']}")
                    sleep(delay + random())
        except Exception as e:
            print(e.args)
            sleep(delay + random())

if __name__ == "__main__":

    print("\n------------Информация-----------")
    print("Создатель бота VoprosiKira")
    print("По вопросам:")
    print("VK_id: voprosikiraz")
    print("TG: @MarchFox")
    print("---------------------------------")

    # Конфиг
    with open("config.json") as f:
        try:
            config = load(f)
        except:
            print("Неверный конфиг")
            sys.exit()
    auth = str(config["authorization"])
    conf_buy_fetters = int(config["buy_fetters"])
    conf_buy_slaves = int(config["buy_slaves"])
    give_job = int(config["give_job"])
    top_hate = int(config["top_hate"])
    delay = int(config["delay"])
    try:
        job = list(config["job"])
    except:
        job = str(config["job"])
    max_price = int(config["max_price"])
    my_id = int(config["my_id"])
    conf_upgrade_slaves = int(config["upgrade_slaves"])

    # Переменные

    print("------------Настройки------------")
    if conf_buy_slaves == 1:
        print("Покупка случайных рабов = ВКЛ")
        Thread(target=buy_slaves).start()
    if conf_buy_slaves == 0:
        print("Покупка случайных рабов = ВЫКЛ")
    if top_hate == 1:
        print("Перекупка рабов у топеров = ВКЛ")
        Thread(target=buy_top_users_slaves).start()
    if top_hate == 0:
        print("Перекупка рабов у топеров = ВЫКЛ")
    if give_job == 1:
        print("Авто-назначение работы = ВКЛ")
        Thread(target=job_slaves).start()
    if give_job == 0:
        print("Авто-назначение работы = ВЫКЛ")
    if conf_buy_fetters == 1:
        print("Авто-покупка оков = ВКЛ")
        Thread(target=buy_fetters).start()
    if conf_buy_fetters == 0:
        print("Авто-покупка оков = ВЫКЛ")     
    if conf_upgrade_slaves == 1:
        print("Авто-прокачка рабов = ВКЛ")
        Thread(target=upgrade_slaves).start()
    if conf_upgrade_slaves == 0:
        print("Авто-прокачка рабов = ВЫКЛ")      
    print("---------------------------------\n")
    os.system("pause")
    print("")