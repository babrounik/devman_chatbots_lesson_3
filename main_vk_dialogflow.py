import os
import random
from dotenv import load_dotenv

import vk_api as vk
from google.cloud import dialogflow
from vk_api.longpoll import VkLongPoll, VkEventType


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
    return response.query_result.fulfillment_text


def echo(event, vk_api):
    project_id = os.getenv("DIALOGFLOW_PROJECT")
    session_id = os.getenv("ARTSIOM_CHAT_ID")
    texts = event.text
    language_code = "RU"
    response = detect_intent_texts(project_id, session_id, texts, language_code)
    reply_text = response

    vk_api.messages.send(
        user_id=event.user_id,
        message=reply_text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    load_dotenv("./.env")
    vk_token = os.getenv("VK_COM")
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
