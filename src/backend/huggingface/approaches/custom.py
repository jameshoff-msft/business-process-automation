from approaches.agents.custom import FakeAgent
from approaches.approach import Approach
from approaches.chains.custom import CustomChain
from approaches.retrievers.cogsearchfacetsretriever import CogSearchFacetsRetriever

from langchain.callbacks.base import BaseCallbackHandler
from langchain.agents import AgentType, initialize_agent, AgentOutputParser
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from langchain.tools import Tool
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.callbacks.stdout import StdOutCallbackHandler
from typing import Any, Dict, List, Union
from langchain.schema import AgentAction, AgentFinish, LLMResult
import re
import json

import os
from approaches.retrievers.cogsearchretriever import CogSearchRetriever
from approaches.retrievers.vectorretriever import VectorRetriever

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2022-12-01"
os.environ["OPENAI_API_BASE"] = "https://"+os.environ["AZURE_OPENAI_SERVICE"]+".openai.azure.com"

callback_sandbox = {}
count = 0

class MyCallbackHandler(BaseCallbackHandler):
    """Base callback handler that can be used to handle callbacks from langchain."""
    def __init__(self):
        self.steps : List[str] = []

    def get_prompts(self) -> List[str]:
        return self.steps
    
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""
        self.steps = self.steps + prompts

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors."""

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        """Run when chain starts running."""

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""

    def on_chain_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when chain errors."""

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Run when tool starts running."""

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        """Run when tool ends running."""

    def on_tool_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when tool errors."""

    def on_text(self, text: str, **kwargs: Any) -> Any:
        """Run on arbitrary text."""

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        """Run on agent end."""
    
class CustomApproach(Approach):
    def __init__(self, index: any):
        self.index = index

    def get_memory(self, history):
        memory = ConversationBufferMemory()
        for i in history:
            if "bot" in i:
                memory.chat_memory.add_ai_message(i["bot"])
            if "user" in i:
                memory.chat_memory.add_ai_message(i["user"])
        return memory
    
    def get_history_string(self, history):
        output = ""
        for i in history:
            if "user" in i:
                #memory.chat_memory.add_ai_message(i["user"])
                output = output + "\nUser: " + i["user"] + "\n"
            if "bot" in i:
                output = output + "\nBot: " + i["bot"] + "\n"
                #memory.chat_memory.add_ai_message(i["bot"])
            
        return output

    def get_thought_string(self, intermediate_steps):
        thoughts = ""
        data_points = []
        try:
            
            for i in intermediate_steps:
                for j in i:
                    if isinstance(j, str):
                        data_points.append("<br> Observation: " +step + "</br>")
                        thoughts = thoughts + "<br> Observation: " +step + "</br>"
                    else :
                        for step in j:
                            if isinstance(step, str):
                                data_points.append("<br> " +step + "</br>")
                                thoughts = thoughts + "<br> " +step + "</br>"
                  
        except:
            thoughts = ""
        return thoughts, data_points

    def run(self, history: list[dict], overrides: dict) -> any:
        handler = MyCallbackHandler()
        local_count = count
        llm = OpenAI(temperature=0.0,deployment_id=os.environ.get("AZURE_OPENAI_GPT_DEPLOYMENT"),callbacks=[handler])


        # chain = CustomChain(
        #     prompt=PromptTemplate.from_template('tell us a joke about {topic}'),
        #     llm=llm
        # )

        #myout = chain.run({'topic': 'callbacks'}, callbacks=[StdOutCallbackHandler()])

        
#         tools = [
#             Tool( 
#                     name = "Custom Chain",
#                     func=chain.run,
#                     description="useful for when you need to answer questions."
#                 )
#         ]
#         agent = FakeAgent("foo")
#         tool_names = [tool.name for tool in tools]
#         agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, allowed_tools=tool_names)
#         agentOut = agent_executor.run("How many people live in canada as of 2023?")

#         q = history[-1]["user"]
#         memory = self.get_memory(history)
#         #llm = OpenAI(temperature=0.0,deployment_id=os.environ.get("AZURE_OPENAI_GPT_DEPLOYMENT"), batch_size=3)
#         prompt_prefix = """<|im_start|>system
# Assistant helps answer questions within text from documents. Be brief in your answers.
# Answer ONLY with the facts listed in the list of sources below. If there isn't enough information below, say you don't know. Do not generate answers that don't use the sources below.
# Each source has a name followed by colon and the actual information, always include the source name for each fact you use in the response. Use square brakets to reference the source, e.g. [info1.txt]. Don't combine sources, list each source separately, e.g. [info1.txt][info2.pdf].
# Sources:

# <|im_end|>

# """
     

        def lookup(input):
            return input
        
        q = history[-1]["user"]
        # template=""" 
        # Chat History:
        # {history}

        # Current Question:
        # {q}

        # Generate a detailed question that uses the information in the Chat History to remove any ambiguity.   The questions should be in the context of the Ferrari 458.  Add all additional entities to the search that will find the correct page within the user manual.
        # """
        # prompt = PromptTemplate(
        #     input_variables=["history","q"],
        #     template=template,
        # )
        # prompt_string = prompt.format(history=self.get_history_string(history), q=q)

        # my_new_prompt = llm(prompt_string)
        
       
        tools = []
        # tools.append(Tool( 
        #             name = "Lookup",
        #             func=lookup,
        #             description="useful for when you need to lookup terms",
        #             return_direct=True
        #         ))
        if len(overrides.get("vector_search_pipeline")) > 2: 
            vector_retriever = VectorRetriever(overrides.get("vector_search_pipeline"), str(overrides.get("top")))
            qa = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, chain_type="refine", retriever=vector_retriever)
            # tools.append(Tool( 
            #         name = "Search",
            #         func=qa.run,
            #         description="useful for when you need to search for information in documents",
            #         return_direct=True
            #     ))
            #agent = initialize_agent(tools, llm, agent=AgentType.REACT_DOCSTORE, verbose=True ,return_intermediate_steps=True)
            # qa_vector = RetrievalQA.from_chain_type(llm=llm, chain_type="refine", retriever=vector_retriever)
            # tools.append(Tool(
            #         name = "Vector Search",
            #         func=qa_vector.run,
            #         description="useful for when you need to answer questions."
            #     ))
        else:
            retriever = CogSearchRetriever(self.index,self.index.get("searchableFields"), overrides.get("top"))
            qa = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, chain_type="refine", retriever=retriever)
            # retriever_facets = CogSearchFacetsRetriever(self.index,self.index.get("searchableFields"), overrides.get("top"))
            # qa_facets = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever_facets)
            # tools.append(Tool(
            #         name = "Cognitive Search",
            #         func=qa.run,
            #         description="useful for when you need to answer questions",
            #         return_direct=True
            #     ))
            # tools.append(Tool(
            #         name = "Cognitive Search Facets",
            #         func=qa_facets.run,
            #         description="useful to get sentiment data for the results of a query"
            #     ))

        
        out = qa({"question" : q + " Each source has a name followed by colon and the actual information, always include the source name for each fact you use in the response. Use square brakets to reference the source, e.g. [info1.txt]. Don't combine sources, list each source separately, e.g. [info1.txt][info2.pdf]."})

        sources = re.findall(r'\[(.*?)\]',out["answer"])
        parsedSources = []
        answer = out["answer"]
        for s in sources:
            split_s = s.split('/')
            doc_path = split_s[len(split_s)-1].replace('.txt','')
            answer = answer.replace(split_s[len(split_s)-1], split_s[len(split_s)-1].replace('.txt',''))
            parsedSources.append(doc_path)

        # agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, return_intermediate_steps=True, max_iterations=3, input_variables=["sources", "chat_history", "input"])
        # out = agent({"input" : q})
        prompts = handler.get_prompts()
        thoughts = '.'.join(str(x) for x in prompts)
        #thoughts, data_points = self.get_thought_string(out["intermediate_steps"])
        return {"data_points": handler.get_prompts(), "answer": out["answer"], "thoughts": thoughts}