import os
import vk_api
import random

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

load_dotenv("./.env")
vk_token = os.getenv("VK_COM")
vk_session = vk_api.VkApi(token=vk_token)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print('Новое сообщение:')
        if event.to_me:
            print('Для меня от: ', event.user_id)
        else:
            print('От меня для: ', event.user_id)
        print('Текст:', event.text)
        vk.messages.send(random_id=10001,
                         user_id=event.user_id, message='Привет, человек!')
