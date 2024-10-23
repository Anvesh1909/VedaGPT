from transformers import AutoTokenizer


import torch

import os

import warnings
warnings.filterwarnings('ignore')
from ..models import LLM_models
from asgiref.sync import sync_to_async

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


@sync_to_async
def LLM_reply(prompt, context=None,  ModelName = "Llama2"):
    # print(context)
    torch.cuda.empty_cache()

    try:
        # Retrieve LLM Model Details
        model = LLM_models.objects.get(name=ModelName)

        if context:
            model_prompt_template = model.pdf_prompt
            prompt_text = model_prompt_template.format(prompt=prompt, context=context)
        else:
            model_prompt_template = model.prompt
            prompt_text = model_prompt_template.format(prompt=prompt, context="")

        print(f"Model name: {model.name}, Model key: {model.modelKEY}, Path: {model.file_path}")

        # LLM Model Loading with Error Handling
        try:
            llm = model.modelKEY
            modelPath = model.file_path
            cache_dir = os.path.join(modelPath, model.name)

            # quantization_config = BitsAndBytesConfig(load_in_8bit=True)
            bnb_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.bfloat16
                )
            
            model = AutoModelForCausalLM.from_pretrained(
                llm,
                cache_dir=cache_dir,
                quantization_config=bnb_config,
                device_map="auto",
            )

            tokenizer = AutoTokenizer.from_pretrained(
                llm,
                cache_dir=cache_dir
            )
        except Exception as e:
            print(f"Error loading LLM model: {e}")
            return "Error: Could not load the LLM model."

        # Prompt Tokenization
        inputs = tokenizer(prompt_text, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

        # LLM Model Inference
        try:
            outputs = model.generate(**inputs, temperature=0.001 , max_new_tokens=1024)
            response = tokenizer.decode(outputs[0])
        except Exception as e:
            print(f"Error during LLM inference: {e}")
            return "Error: An error occurred while processing your request."

        # Response Trimming
        print("\n before",response)
        response = response[len(prompt_text)+5:]
        response = markdown_to_html(response)
        print(response)
        # Memory Cleanup
        torch.cuda.empty_cache()
    
        return response

    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Error: An unexpected error occurred."
    
    
        
        
       
        



import re

def markdown_to_html(text):
    # Convert bold text
    bold_pattern = re.compile(r'\*\*(.*?)\*\*')
    text = re.sub(bold_pattern, r'<strong>\1</strong>', text)

    # Convert code blocks
    code_block_pattern = re.compile(r'```(.*?)```', re.DOTALL)
    text = re.sub(code_block_pattern, r'<pre><code>\1</code></pre>', text)
    
    return text


    