import json
import os
from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main() -> None:
    load_dotenv(".env")
    project_id = os.getenv("DIALOGFLOW_PROJECT")
    path_to_questions = os.getenv['QUESTIONS_PATH']
    with open(path_to_questions) as file_with_questions:
        questions_file_content = file_with_questions.read()

    questions_file_content = json.loads(questions_file_content)

    for display_name in questions_file_content:
        training_phrases_parts = questions_file_content[display_name]['questions']
        message_texts = questions_file_content[display_name]['answer']
        create_intent(project_id, display_name, training_phrases_parts, [message_texts])


if __name__ == '__main__':
    main()
