import openai
import json
import sqlite3
import uuid
import datetime
import copy

from app.functions import log, getConfig


class OpenAIManager:
    def __init__(self, module_manager):
        self.module_manager = module_manager
        self.messages = []  # to send
        self.conversation = {"id": None, "timestamp": None, "tokens": 0, "messages": []}
        self.functions = self.module_manager.function_instances
        self.functionsToSend = []
        self.chatCompletion = None
        self.chatCompletionMessage = None

        self.newSession()
        self.setupTables()

    def addMessage(self, object):
        self.messages.append(copy.deepcopy(object))
        object["id"] = str(uuid.uuid4())
        object["timestamp"] = datetime.datetime.now().isoformat()
        object["tokens"] = object.get("tokens", 0)
        self.conversation["messages"].append(object)

    def reloadFunctions(self):
        self.functions = copy.deepcopy(self.module_manager.function_instances)
        self.functionsToSend = []

        for function in self.functions:
            self.functionsToSend.append(
                {
                    "name": f"{function.type}-{function.module}-{function.name}",
                    "description": function.description,
                    "parameters": function.parameters,
                }
            )

    def newSession(self):
        # add logic here later to save previous conversation for training purposes
        if len(self.messages) > 1:
            self.saveConversation()

        self.reloadFunctions()
        self.conversation = {"id": None, "timestamp": None, "messages": []}
        self.messages = []
        self.addMessage(
            {
                "role": "system",
                "content": getConfig()["initialPrompt"],
            }
        )

        # INITIALIZE CONVERSATION
        self.conversation["id"] = str(uuid.uuid4())
        self.conversation["tokens"] = 0

    def newUserMessage(self, message):
        if len(self.messages) == 1:
            self.conversation["timestamp"] = datetime.datetime.now().isoformat()

        self.addMessage({"role": "user", "content": message})
        self.runChatCompletion()

        if self.chatCompletionMessage.get("function_call"):
            # Call the function
            function_string = self.chatCompletionMessage["function_call"]["name"]
            function_type = function_string.split("-")[0]
            function_module = function_string.split("-")[1]
            function_name = function_string.split("-")[2]
            log(
                f"Calling Function: \n\tTYPE: {function_type} MODULE: {function_module} NAME: {function_name}",
                color="HEADER",
            )
            function_to_run = self.module_manager.getFunctionByName(
                function_type, function_module, function_name
            )
            function_response = function_to_run.handle(
                json.loads(self.chatCompletionMessage["function_call"]["arguments"])
            )

            if not function_response:
                function_response = "Success"

            return self.handleFunctionResponse(
                self.chatCompletionMessage, function_response
            )

        return self.chatCompletionMessage["content"]

    def runChatCompletion(self):
        log("Running chat completion")

        openai.api_key = getConfig()["openaiKey"]

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            functions=self.functionsToSend,
        )

        log(f"Total tokens: {completion['usage']}", color="HEADER")

        self.chatCompletion = completion
        self.chatCompletionMessage = completion["choices"][0]["message"]
        self.messages.append(self.chatCompletionMessage)

        conversationMessage = copy.deepcopy(self.chatCompletionMessage)
        conversationMessage["id"] = str(uuid.uuid4())
        conversationMessage["tokens"] = completion["usage"]["total_tokens"]
        conversationMessage["timestamp"] = datetime.datetime.now().isoformat()

        self.conversation["messages"].append(conversationMessage)
        self.conversation["tokens"] += completion["usage"]["total_tokens"]

    def handleFunctionResponse(self, functionCall, functionResponse):
        functionName = functionCall["function_call"]["name"]

        self.addMessage(
            {
                "role": "function",
                "name": functionName,
                "content": functionResponse,
            }
        )

        for function in self.functions:
            function_type = functionName.split("-")[0]
            function_module = functionName.split("-")[1]
            function_name = functionName.split("-")[2]
            if (
                (function_type == function.type)
                & (function_module == function.module)
                & (function_name == function.name)
            ):
                self.functionsToSend = [
                    {
                        "name": f"{function.type}-{function.module}-{function.name}",
                        "description": function.description,
                        "parameters": function.parameters,
                    }
                ]

        self.runChatCompletion()
        return self.chatCompletionMessage["content"]

    def setupTables(self):
        connection = sqlite3.connect("databases/conversations.db")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS Conversations (
                ConversationID TEXT PRIMARY KEY,
                Tokens INTEGER NOT NULL,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS Messages (
                MessageID TEXT PRIMARY KEY,
                ConversationID TEXT,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                Role TEXT NOT NULL,
                Content TEXT NOT NULL,
                Function TEXT,
                Arguments TEXT,
                Tokens INTEGER,
                FOREIGN KEY(ConversationID) REFERENCES Conversations(ConversationID)
            );
            """
        )

        connection.close()

    def saveConversation(self):
        log(self.conversation, color="OKCYAN")
        connection = sqlite3.connect("databases/conversations.db")
        cursor = connection.cursor()

        # Save the conversation
        cursor.execute(
            "INSERT INTO Conversations (ConversationID, Tokens, Timestamp) VALUES (?, ?, ?)",
            (
                self.conversation["id"],
                self.conversation["tokens"],
                self.conversation["timestamp"],
            ),
        )

        # Save the messages
        for message in self.conversation["messages"]:
            if message.get("content") is None:
                message["content"] = "None"
            cursor.execute(
                """INSERT INTO Messages (MessageID, ConversationID, Timestamp, Role, Content, Function, Arguments, Tokens)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    message.get("id"),
                    self.conversation["id"],
                    message.get("timestamp"),
                    message.get("role"),
                    message.get("content"),
                    message.get("function_call", {}).get("name"),
                    message.get("function_call", {}).get("arguments"),
                    message.get("tokens"),
                ),
            )
        connection.commit()
        connection.close()
