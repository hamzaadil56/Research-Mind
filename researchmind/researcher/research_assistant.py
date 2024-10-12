from langchain_community.tools import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig, chain
import datetime
from dotenv import load_dotenv


class AIResearchAssistant:
    def __init__(self):
        load_dotenv()
        self.llm = ChatOpenAI(model="gpt-4-1106-preview")
        self.tool = self._setup_search_tool()
        self.prompt = self._setup_prompt()
        self.llm_with_tools = self.llm.bind_tools([self.tool])
        self.llm_chain = self.prompt | self.llm_with_tools
        self.tool_chain = self._setup_tool_chain()

    def _setup_search_tool(self):
        return TavilySearchResults(
            max_results=5,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True,
            include_images=True,
        )

    def _setup_prompt(self):
        today = datetime.datetime.today().strftime("%D")
        return ChatPromptTemplate(
            [
                ("system", f"You are a helpful assistant. The date today is {
                 today}."),
                ("human", "{user_input}"),
                ("placeholder", "{messages}"),
            ]
        )

    def _setup_tool_chain(self):
        @chain
        def tool_chain(user_input: str, config: RunnableConfig = None):
            input_ = {"user_input": user_input}
            ai_msg = self.llm_chain.invoke(input_, config=config)
            tool_msgs = self.tool.batch(ai_msg.tool_calls, config=config)
            return self.llm_chain.invoke({**input_, "messages": [ai_msg, *tool_msgs]}, config=config)
        return tool_chain

    def research(self, query: str):
        response = self.tool_chain.invoke(query)
        return response.content


# Usage
# if __name__ == "__main__":
#     assistant = AIResearchAssistant()
#     result = assistant.research(
#         "Can you bring few research papers with its links of how to make epoxy adhesives?")
#     print(result)
