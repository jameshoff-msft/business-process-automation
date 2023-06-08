from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline

gpttokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
gptmodel = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")

class HuggingFaceLLM:

    def analyze(self, text):
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = gpttokenizer.encode(text + gpttokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = gptmodel.generate(new_user_input_ids, max_length=1000, pad_token_id=gpttokenizer.eos_token_id)

        # pretty print last ouput tokens from bot
        out = "{}".format(gpttokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True))

        # nlp = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        # out = nlp(text)
        return {"textOut" : out, "embedding" : chat_history_ids.data}
        