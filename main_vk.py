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
    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text
    else:
        return None


def reply(_event, _vk_api, _project_id, _session_id, _language_code):
    texts = _event.text
    response = detect_intent_texts(_project_id, _session_id, texts, _language_code)

    if response:
        _vk_api.messages.send(
            user_id=_event.user_id,
            message=response,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    load_dotenv("./.env")
    vk_token = os.getenv("VK_COM")
    project_id = os.getenv("DIALOGFLOW_PROJECT")
    session_id = f'vk-{os.getenv("ARTSIOM_CHAT_ID")}'
    LANGUAGE_CODE = "RU"
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply(event, vk_api, project_id, session_id, LANGUAGE_CODE)
