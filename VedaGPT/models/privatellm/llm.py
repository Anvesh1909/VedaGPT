import torch
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
import os
from ..models import LLM_models

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(torch.cuda.is_available())
# models ={
#     "Gemma" : "google/gemma-7b",
#     "Laama" : "meta-llama/Llama-2-7b-chat-hf",
# }





def LLM_reply(prompt, context = None ,  Model_id = 1 ,max_new_tokens=500):

    model = LLM_models.objects.get( id = Model_id )

    if context :
        prompt = f'''
                    [INST]
                    Give an answer for the question strictly based on the context provided.
                    you are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.
                    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
                    If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
                    Question: {prompt}

                    Context : {context}
                    [/INST]
                '''
    else:
        prompt = f'''
                    [INST]
                    you are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.
                    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
                    If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
                    Question: {prompt}
                    [/INST]
                '''


    print(f"model name : {model.name} , model = {model.modelKEY} , path = {model.file_path}")

    llm = model.modelKEY
    modelPath = model.file_path

    print(llm,modelPath)
    # model = AutoModelForCausalLM.from_pretrained(
    #     f"{llm}",
    #     cache_dir=f"{modelPath}",
    #     device_map='auto'
    # )

    # tokenizer = AutoTokenizer.from_pretrained(
    #                                             f"{llm}", 
    #                                             cache_dir=f"{modelPath}"
    #                                      )

    # inputs = tokenizer(prompt, return_tensors="pt").to(device)
    # outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, temperature= 0.00001)
    # response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = prompt
    return response