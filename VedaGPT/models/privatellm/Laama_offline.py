import os
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM

import torch
import re


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", 
                                          cache_dir="/data/VedaGPT/base_models"
                                         )


def get_llama2_chat_reponse(prompt, max_new_tokens=50):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, temperature= 0.00001)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    cache_dir="/data/VedaGPT/base_models",
    device_map='auto'
)

def reply(user_prompt):
    print("Entered replyPdf: Laama.py")
    query = user_prompt

    prompt = f'''
    [INST]
    Give answer for the question strictly based on the context provided. Keep answers short and to the point.

    Question: {query}

    
    [/INST]
    '''
    result = get_llama2_chat_reponse(prompt, max_new_tokens=80)
    print("Model Reply:")
    result = re.sub(r'\[INST\].*?\[/INST\]', '', result)
    print(result)
    return result



def replyPdf(user_prompt, context):
    print("Entered replyPdf: Laama.py")
    
    query = user_prompt

    prompt = f'''
    [INST]
    Give answer for the question strictly based on the context provided. Keep answers short and to the point.

    Question: {query}

    Context : {context}
    [/INST]
    '''
    result = get_llama2_chat_reponse(prompt, max_new_tokens=80)
    print("Model Reply:")
    result = re.sub(r'\[INST\].*?\[/INST\]', '', result)
    print(result)
    return result
