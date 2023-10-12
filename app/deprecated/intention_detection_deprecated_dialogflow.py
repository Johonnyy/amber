from google.cloud import dialogflow
from app.functions import log
from app.assistant.handlers import *
import uuid
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""


def new_session(sessionId=str(uuid.uuid4())):
    if sessionId == None:
        sessionId = str(uuid.uuid4())
    print("sessionId: " + str(sessionId))
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path("amber-vlpl", sessionId)
    return session, session_client, sessionId


def detect_intention(text, oldSessionId=None, interactive=False):
    print("oldSessionId: " + str(oldSessionId))
    session, session_client, sessionId = new_session(oldSessionId)
    response = send_input(text, session, session_client)
    print(response.query_result.fulfillment_text)
    if not response.query_result.all_required_params_present:
        log("true")

        return {
            "text": response.query_result.fulfillment_messages[0].text.text[0],
            "requiresEntity": True,
            "sessionId": sessionId,
        }
        # dialogflow tells you that all require params are present so just pass the fulfillment text and session id to device
    else:
        fields = {}

        parameters_dict = dict(response.query_result.parameters)
        for key, value in parameters_dict.items():
            if value:  # Only add non-empty entities
                fields[key] = {"value": value}

        intent = response.query_result.intent.display_name

        log("intent: " + str(intent))
        log("fields: " + str(fields))

        if not intent or not fields:
            return {
                "text": response.query_result.fulfillment_messages[0].text.text[0],
                "requiresEntity": False,
            }

        handleResponse = handle_intent(intent, fields, text)

        if handleResponse.get("overwrite", False):
            return {
                "text": handleResponse.get("message", ""),
                "requiresEntity": False,
            }
        else:
            return {
                "text": response.query_result.fulfillment_messages[0].text.text[0],
                "requiresEntity": False,
            }


def send_input(text, session, session_client):
    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response


def handle_intent(intent=None, entities=None, userMessage=None):
    log("handle intent")
    intentCategory, intentName = intent.split(".")

    log(intentCategory)
    log(intentName)

    if intentCategory == "config":
        return handle_config(intentName, entities)
    elif intentCategory == "weather":
        return handle_weather(intentName, entities, userMessage)
    elif intentCategory == "plugin":
        return handle_plugin(intentName, entities)
    # Checked all built in intents

    from app.extensions import extensions

    plugin = extensions.plugin_manager.get_plugin_by_name(intentCategory)
    if plugin:
        plugin.handle(intentName, entities)
        return {
            "overwrite": False,
        }

    pluginData = extensions.plugin_manager.get_plugin_data_by_name(intentCategory)
    log(pluginData)
    if pluginData:
        return {
            "overwrite": True,
            "message": f"The {pluginData['displayName']} plugin is not enabled.",
        }
