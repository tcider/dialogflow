#https://dialogflow.cloud.google.com/cx/projects/dialogflow-293713/locations/global/agents/b652d899-c8b9-4f90-91f5-2106ff9373a0

import argparse
import uuid

from google.cloud.dialogflowcx_v3beta1.services.agents import AgentsClient
from google.cloud.dialogflowcx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3beta1.types import session

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="infostart-ru-a97c6e80d3a7.json"
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="client_secret_526406941140-sv9snv8khetn2qlsb0mctm8kobreeps2.apps.googleusercontent.com.json"


# [START dialogflow_detect_intent_text]
def run_sample():
    # agent = "projects/dialogflow-293713/locations/global/agents/b652d899-c8b9-4f90-91f5-2106ff9373a0"
    project_id = "dialogflow-293713"
    location_id = "global"
    agent_id = "b652d899-c8b9-4f90-91f5-2106ff9373a0"
    agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"

    session_id = uuid.uuid4()
    texts = ["Привет"]
    language_code = "ru-ru"

    detect_intent_texts(agent, session_id, texts, language_code)


def detect_intent_texts(agent, session_id, texts, language_code):
    session_path = f"{agent}/sessions/{session_id}"
    print(f"Session path: {session_path}\n")
    client_options = None
    agent_components = AgentsClient.parse_agent_path(agent)
    location_id = "global"
    if location_id != "global":
        api_endpoint = f"{location_id}-dialogflow.googleapis.com:443"
        print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)

    for text in texts:
        text_input = session.TextInput(text=text)
        query_input = session.QueryInput(text=text_input, language_code=language_code)
        request = session.DetectIntentRequest(
            session=session_path, query_input=query_input
        )
        response = session_client.detect_intent(request=request)

        print("=" * 20)
        print(f"Query text: {response.query_result.text}")
        response_messages = [
            " ".join(msg.text.text) for msg in response.query_result.response_messages
        ]
        print(f"Response text: {' '.join(response_messages)}\n")


def default_start():

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--agent", help="Agent resource name.  Required.", required=True
    )
    parser.add_argument(
        "--session-id",
        help="Identifier of the DetectIntent session. " "Defaults to a random UUID.",
        default=str(uuid.uuid4()),
    )
    parser.add_argument(
        "--language-code",
        help='Language code of the query. Defaults to "en-US".',
        default="en-US",
    )
    parser.add_argument("texts", nargs="+", type=str, help="Text inputs.")

    args = parser.parse_args()

    detect_intent_texts(args.agent, args.session_id, args.texts, args.language_code)


def main():

    run_sample()


if __name__ == "__main__":
    main()
