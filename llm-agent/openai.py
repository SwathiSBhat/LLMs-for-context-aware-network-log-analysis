import os

from dotenv import load_dotenv
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from log_extractor import getlogs
from thought import create_tree_of_thought_prompts


class GPTAgent:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model = ChatOpenAI(model="gpt-3.5-turbo-0125")
        self.vectorstore = self._create_vectorstore()
        self.retriever = self.vectorstore.as_retriever()
        self.prompt_template = self._create_prompt_template()
        self.output_parser = StrOutputParser()
        self.chain = self._create_chain()

    def _create_vectorstore(self):
        return DocArrayInMemorySearch.from_texts(
            ["about log", "about log"],
            embedding=OpenAIEmbeddings(),
        )

    def _create_prompt_template(self):
        template = f"""Answer the question based only on the following context:
                    {getlogs(0, 0)}
                    Question: {create_tree_of_thought_prompts()}
                    """
        return ChatPromptTemplate.from_template(template)

    def _create_chain(self):
        setup_and_retrieval = RunnableParallel(
            {"context": self.retriever, "question": RunnablePassthrough()}
        )
        return setup_and_retrieval | self.prompt_template | self.model | self.output_parser

    def ask_question(self, question):
        return self.chain.invoke(question)
