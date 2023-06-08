from typing import Any, List, Mapping, Optional
from HuggingFaceLLM import HuggingFaceLLM
from approaches.callback import MyCallbackHandler

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM

class CustomLLM(LLM):
    callback : MyCallbackHandler
    n : int
        
    @property
    def _llm_type(self) -> str:
        return "custom"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        llm = HuggingFaceLLM()
        self.callback.on_llm_start([],[prompt])
        out = llm.analyze(prompt)
        
        return out["textOut"]
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": self.n}