import PyPDF2
import os
from ..models import LLM_models
from asgiref.sync import sync_to_async
from langchain.document_loaders import PyPDFLoader
import os
from django.conf import settings

from transformers import AutoTokenizer

import torch

import os

import warnings
warnings.filterwarnings('ignore')
from ..models import LLM_models
from asgiref.sync import sync_to_async

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig





@sync_to_async
def summarizer(text, ModelName = "Llama2"):
        torch.cuda.empty_cache()
        model = LLM_models.objects.get(name=ModelName)

        llm = model.modelKEY
        modelPath = model.file_path
        cache_dir = os.path.join(modelPath, model.name)
        # for i in chunks[0]:
        torch.cuda.empty_cache()
        
            # You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
            #         You are a very good author and writer who is proficient in writing summaries, research papers and novels. 
        model_prompt_template = model.summarization_prompt
        prompt = model_prompt_template.format(text=text)
        try:
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
        
        try:
            inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

            # LLM Model Inference
            try:
                outputs = model.generate(**inputs, temperature=0.0001 , max_new_tokens=1024)
                response = tokenizer.decode(outputs[0])
            except Exception as e:
                print(f"Error during LLM inference: {e}")
                return "Error: An error occurred while processing your request."
            response = response[len(prompt)+5:]
            response = markdown_to_html(response)
            del model,tokenizer,outputs
            torch.cuda.empty_cache()
            print(response)
        except Exception as e:
            print(f"Error during LLM inference: {e}")
            torch.cuda.empty_cache()
            return "Error: An error occurred while processing your request."

    

        return response
    
   

import re

def markdown_to_html(text):
    # Convert bold text
    bold_pattern = re.compile(r'\*\*(.*?)\*\*')
    text = re.sub(bold_pattern, r'<strong>\1</strong>', text)

    # Convert code blocks
    code_block_pattern = re.compile(r'```(.*?)```', re.DOTALL)
    text = re.sub(code_block_pattern, r'<pre><code>\1</code></pre>', text)
    
    return text 
    
@sync_to_async
def text_chunks(text, chunk_size=4000):
    # Check if the input text is valid
    if not isinstance(text, str):
        raise ValueError("Input text must be a string")
    
    # Get the length of the text
    text_length = len(text)
    
    # Initialize an empty list to store the chunks
    chunks = []
    
    # Loop through the text and slice it into chunks of the specified size
    for i in range(0, text_length, chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    
    return chunks

@sync_to_async
def Chunking(path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    reader = PyPDF2.PdfReader(file_path)

    # Extract text from each page and concatenate
    pages = [page.extract_text() for page in reader.pages]
    document = '\n'.join(pages)

    # Split the document into overlapping chunks
    chunks = get_overlapped_chunks(document, 1000, 0)
    print("chunks:")
    print(chunks)
    return chunks


def get_overlapped_chunks(textin, chunksize, overlapsize):  
    # Generate overlapping chunks of text
    return [textin[a:a+chunksize] for a in range(0, len(textin), chunksize-overlapsize)]
 