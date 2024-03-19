import torch
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

models ={
    "Gemma" : "google/gemma-7b",
    "Laama" : "meta-llama/Llama-2-7b-chat-hf",
}





def LLM_reply(prompt, Name = "Laama" ,max_new_tokens=50):

    model=models[Name]

    print(f"model name : {Name} , model = {model}")

    # model = AutoModelForCausalLM.from_pretrained(
    #     "{model}",
    #     cache_dir="/data/{Name}/base_models",
    #     device_map='auto'
    # )

    # tokenizer = AutoTokenizer.from_pretrained("{model}", 
    #                                       cache_dir="/data/{Name}/base_models"
    #                                      )

    # inputs = tokenizer(prompt, return_tensors="pt").to(device)
    # outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, temperature= 0.00001)
    # response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = "hello"
    
    return response