import argparse
import os
import random
from dotenv import load_dotenv

import vk_api as vk
from dialogflow import detect_intent_texts
from vk_api.longpoll import VkLongPoll, VkEventType


def reply(_event, _vk_api, _project_id, _language_code):
    response = detect_intent_texts(_project_id, _event.user_id, _event.text, _language_code)

    if response:
        _vk_api.messages.send(
            user_id=_event.user_id,
            message=response,
            random_id=random.randint(1, 1000)
        )


def main() -> None:
    load_dotenv("./.env")
    vk_token = os.getenv("VK_COM")
    project_id = os.getenv("DIALOGFLOW_PROJECT")
    language_code = "RU"
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply(event, vk_api, project_id, language_code)


if __name__ == "__main__":
    main()
