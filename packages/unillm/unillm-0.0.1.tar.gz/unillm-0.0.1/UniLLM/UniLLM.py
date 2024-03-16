import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from openai import OpenAI
from peft import PeftModel  # 确保已安装peft库
import os

class UniLLMBase:
    def generate_response(self, message):
        raise NotImplementedError("This method should be implemented by subclasses.")

class ChatGPT(UniLLMBase):
    def __init__(self, api_key, model_name="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
    
    def generate_response(self, message):
        response = self.client.chat.completions.create(
            model=self.model_name, 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content

class Llama(UniLLMBase):
    def __init__(self, model_id='meta-llama/Llama-2-7b-chat-hf', peft_path=None):
        self.model_id = model_id
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map = "cuda" if torch.cuda.is_available() else None)

        if peft_path is not None:
            try:
                self.model = PeftModel.from_pretrained(self.model, peft_path)
                print(f"Loaded PEFT model from {peft_path}")
            except Exception as e:
                print(f"Failed to load PEFT model from {peft_path}: {e}")

    def generate_response(self, message, max_length=512, num_beams=5):
        input_ids = self.tokenizer.encode(message, return_tensors='pt')
        model_device = next(self.model.parameters()).device
        input_ids = input_ids.to(model_device)
        output_ids = self.model.generate(input_ids, max_length=max_length, num_beams=num_beams)
        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

class Mistral(UniLLMBase):
    def __init__(self, model_id="mistralai/Mistral-7B-Instruct-v0.2", tokenizer_id=None):
        self.model_id = model_id
        tokenizer_id = tokenizer_id if tokenizer_id is not None else model_id
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")

    def generate_response(self, message, max_length=512, num_beams=5):
        input_ids = self.tokenizer.encode(message, return_tensors='pt')
        model_device = next(self.model.parameters()).device
        input_ids = input_ids.to(model_device)
        output_ids = self.model.generate(input_ids, max_length=max_length, num_beams=num_beams)
        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

class Claude(UniLLMBase):
    def __init__(self, api_key, model_id="claude-3-opus-20240229"):
        import anthropic
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model_id = model_id
    
    def generate_response(self, message, max_tokens=1000, temperature=0):
        response = self.client.messages.create(
            model=self.model_id,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": message
                        }
                    ]
                }
            ]
        )
        return response.content[0].text


class MistralAI(UniLLMBase):
    def __init__(self, api_key=None, model="mistral-large-latest"):
        from mistralai.client import MistralClient
        from mistralai.models.chat_completion import ChatMessage
        self.ChatMessage = ChatMessage
        self.api_key = api_key if api_key is not None else os.environ.get("MISTRAL_API_KEY")
        self.client = MistralClient(api_key=self.api_key)
        self.model = model
    
    def generate_response(self, message):
        messages = [self.ChatMessage(role="user", content=message)]
        chat_response = self.client.chat(model=self.model, messages=messages)
        return chat_response.choices[0].message.content

class RAG(UniLLMBase):
    def __init__(self, api_key, data_path, ragmodel=None):
        from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
        from llama_index.legacy.llms.ollama import Ollama
        os.environ["OPENAI_API_KEY"] = api_key
        documents = SimpleDirectoryReader(data_path).load_data()
        self.rag_index = VectorStoreIndex.from_documents(documents)
        
        if ragmodel:
            self.rag_query_engine = self.rag_index.as_query_engine(llm=Ollama(model=ragmodel, request_timeout=60.0))
        else:
            self.rag_query_engine = self.rag_index.as_query_engine()
    
    def generate_response(self, message):
        return self.rag_query_engine.query(message)

# Now, integrate RAG into the UniLLM class
class UniLLM:
    def __init__(self, model_type, **kwargs):
        self.model = self.initialize_model(model_type, **kwargs)

    def initialize_model(self, model_type, **kwargs):
        if model_type == 'chatgpt':
            return ChatGPT(**kwargs)
        elif model_type == 'llama':
            return Llama(**kwargs)
        elif model_type == 'mistral':
            return Mistral(**kwargs)
        elif model_type == 'claude':
            return Claude(**kwargs)
        elif model_type == 'mistralai':
            return MistralAI(**kwargs)
        elif model_type == 'rag':
            return RAG(**kwargs)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    def generate_response(self, message):
        return self.model.generate_response(message)


# 示例使用
if __name__ == "__main__":
    # 确保你的api.txt文件路径是正确的
    api_key = open("../../../api.txt").read()
    claude_api = open("../../../claude.txt").read()
    mistral_api = open("../../../mistral.txt").read()

    # 使用 ChatGPT 模型，并指定模型名称
    """chatgpt_bot = UniLLM(model_type='chatgpt', api_key=api_key, model_name="gpt-3.5-turbo")
    print(chatgpt_bot.generate_response("Who are you?"))

    # 使用 LLAMA 模型
    llama_bot = UniLLM(model_type='llama', model_id='meta-llama/Llama-2-7b-chat-hf')
    print(llama_bot.generate_response("Who are you?"))

    # 使用 Mistral 模型
    mistral_bot = UniLLM(model_type='mistral')
    print(mistral_bot.generate_response("What's your name?"))

    # Initialize a UniLLM instance with the Claude model
    claude_bot = UniLLM(model_type='claude', api_key=claude_api)
    print(claude_bot.generate_response("What's your name?"))

    mistralai_bot = UniLLM(model_type='mistralai', api_key=mistral_api)
    print(mistralai_bot.generate_response("What's your name?"))"""

    rag_bot = UniLLM(model_type='rag', api_key=api_key, data_path="../../../output/preprocessed/animal10/raw")
    print(rag_bot.generate_response("What is The Luminous Laionec?"))
