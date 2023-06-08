import logging
import azure.functions as func
from HuggingFaceLLM import HuggingFaceLLM


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    out = {}
    try:
        req_body = req.get_json()
        hf = HuggingFaceLLM()

        out = hf.analyze(req_body.get('text'))
   
    except ValueError:
        logging.info(ValueError)

    return f'{out}'
    

    
        

