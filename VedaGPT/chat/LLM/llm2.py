import os
from ..models import LLM_models
from asgiref.sync import sync_to_async
from django.conf import settings
import torch, transformers
# from langchain_community.document_loaders.unstructured import UnstructuredFileLoader
import warnings
warnings.filterwarnings('ignore')
from ..models import LLM_models
from asgiref.sync import sync_to_async
from transformers import AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import ConversationChain

@sync_to_async
def LLM_reply(input, path=None, ModelName = "Llama2", max_new_tokens=600):
    print("llm.py")
    torch.cuda.empty_cache()
    modeldb = LLM_models.objects.get(name=ModelName)
    llm = modeldb.modelKEY
    modelPath = modeldb.file_path
    cache_dir = os.path.join(modelPath, modeldb.name)
    if path!=None:
        # print(path)
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',model_kwargs={'device': "cuda" if torch.cuda.is_available() else "cpu"})
        text_chunks=text_splitter.split_documents(pages)
        print(text_chunks[0])
        vectorstore=FAISS.from_documents(text_chunks, embeddings)
        retriever = vectorstore.as_retriever()
        # prompt_template = """
        #                 [INST] <<SYS>>
        #                 you are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.
        #                 You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
        #                 If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
        #                 <</SYS>>
        #                 [/INST]
                    
        #     Use the following context and the chat history to answer the question:
        #     Context: {context} 
        #     Question: {question}"""
        prompt_template = """
          <s>[INST] <<SYS>>
            Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand. Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics. Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
          <</SYS>>
          here is the chat history
          {chat_history}

          {input}[/INST]

           """.strip()
        # PROMPT = PromptTemplate(template=prompt_template, input_variables=[ "context",  "question"])
        PROMPT = PromptTemplate(input_variables=["chat_history", "input"], template=prompt_template)
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)
        
        tokenizer = transformers.AutoTokenizer.from_pretrained(
            llm,# PROMPT = PromptTemplate(template=prompt_template, input_variables=[ "context",  "question"])
            cache_dir=cache_dir
        )

        model = AutoModelForCausalLM.from_pretrained(modeldb.modelKEY,
                                               device_map='auto',
                                               quantization_config=quantization_config
                                               )
        pipe = pipeline("text-generation",
                model=model,
                tokenizer= tokenizer,
                device_map="auto",
                max_new_tokens = 1024,
                do_sample=True,
                top_k=10,
                num_return_sequences=1,
                eos_token_id=tokenizer.eos_token_id,
                return_full_text=False
                )
        
        llm=HuggingFacePipeline(pipeline=pipe, model_kwargs={'temperature':0})
        
        
    
        torch.cuda.empty_cache()

        memory = ConversationBufferMemory(memory_key="chat_history",k=3,return_messages=True)
        # doc_qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory)
        doc_qa = ConversationalRetrievalChain.from_llm(llm=llm,retriever=retriever, memory=memory)
        
        # doc_qa = RetrievalQA.from_chain_type(
        #     llm=llm,
        #     chain_type="stuff",
        #     retriever=retriever,
        #     chain_type_kwargs={
        #         "verbose": False,
        #         "prompt": PROMPT,
        #     },
        # )
        
        # query = input(" > ")
        result = doc_qa.invoke(input)
        print("result = ",result)
        return result['answer']
      
    else:
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)
        
        tokenizer = transformers.AutoTokenizer.from_pretrained(
            llm,
            cache_dir=cache_dir
        )

        model = AutoModelForCausalLM.from_pretrained(modeldb.modelKEY,
                                               device_map='auto',
                                               quantization_config=quantization_config
                                               )
        pipe = pipeline("text-generation",
                model=model,
                tokenizer= tokenizer,
                device_map="auto",
                max_new_tokens = 1024,
                do_sample=True,
                top_k=10,
                num_return_sequences=1,
                eos_token_id=tokenizer.eos_token_id,
                return_full_text=False
                )
        
        llm=HuggingFacePipeline(pipeline=pipe, model_kwargs={'temperature':0})
        prompt_template = """
          <s>[INST] <<SYS>>
            Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand. Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics. Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
          <</SYS>>
          here is the chat history
          {chat_history}

          {input}[/INST]

           """.strip()
        PROMPT = PromptTemplate(input_variables=["chat_history", "input"], template=prompt_template)
        
    
        torch.cuda.empty_cache()

        memory = ConversationBufferMemory(memory_key="chat_history",k=1,return_messages=True)
        doc_qa = ConversationChain(llm=llm, memory=memory, prompt = PROMPT)
  
        result = doc_qa.invoke(input)
        print(result)
        return result['response']
    