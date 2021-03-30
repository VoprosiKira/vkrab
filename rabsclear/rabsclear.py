import sys
import time
from json import load
from random import choice, randint, random
from threading import Thread
from requests import get, post
from fake_useragent import UserAgent
ua = UserAgent().random 
auth = "vk_access_token_settings=friends,status&vk_app_id=7794757&vk_are_notifications_enabled=0&vk_is_app_user=1&vk_is_favorite=0&vk_language=ru&vk_platform=desktop_web&vk_ref=catalog_recent&vk_ts=1617106117&vk_user_id=289406032&sign=z_VH1efPaVmbNg9fnMABk-WFuvkjbNZFRil4aNUBhLo"

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

def sell_slaves():
    # Продажа раба
    while True:
        try:
            # Перебор списка рабов
            for slave in get_start()["slaves"]:
                sell_slave(slave["id"])
                print(f"Продал id{slave['id']}")
                time.sleep(2)
        except Exception as e:
            print(e.args)
Thread(target=sell_slaves).start()