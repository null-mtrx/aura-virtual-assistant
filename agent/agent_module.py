from .master import AgentGraph
from PySide6.QtCore import QObject, Signal, Slot

from .vectorstore import VectorStoreHandler
from langchain_core.messages import HumanMessage
import datetime


class AgentInterface(QObject):
    output_tokens = Signal(str)

    def __init__(self):
        super().__init__()
        self.agent = AgentGraph(model="gemini-3-flash-preview")
        self.store = VectorStoreHandler(store_location="./kb")

    @Slot(str)
    def respond_to_query(self, query):
        agent_state = {"messages": [HumanMessage(query)]}

        print("started")
        messages = self.agent.app.invoke(agent_state)
        response = messages["messages"][-1].content[0]["text"]
        self.output_tokens.emit(response)
        self.write_to_history(messages["messages"])

    def write_to_history(self, messages: list):
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        human_message = messages[0]
        ai_response = messages[-1]

        data = {
            "query": {
                "id": f"u_{timestamp}",
                "from": "user",
                "content": human_message.content,
            },
            "response": {
                "id": f"ai_{timestamp}",
                "from": "ai",
                "content": ai_response.content[0]["text"],
            },
        }
        self.store.add_to_knowledge_base(data)
