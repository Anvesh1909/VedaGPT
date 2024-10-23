# views.py

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .models import Chat,Transaction,Documents ,LLM_models
import os

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required







try:
    model_selected = LLM_models.objects.get( name = "Llama2" ) #default first model
except:

    prompt = '''
                        [INST]
                        you are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.
                        You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
                        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
                        Question: {prompt}
                        [/INST]
                    '''
    pdf_prompt='''
        [INST]
                        Give an answer for the question strictly based on the context provided.
                        you are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.
                        You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
                        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
                        Question: {prompt}

                        Context : {context}
                        [/INST]
        '''
    summarization_prompt='''<s>[INST] <<SYS>>
                    write a consise text within 2 points and use bullet point as * and return only text
                    <</SYS>>
                    {text}  [/INST]'''
    llm = LLM_models.objects.create(name="Llama2", modelKEY = "meta-llama/Llama-2-7b-chat-hf", file_path="base_models", prompt = prompt, pdf_prompt = pdf_prompt,summarization_prompt=summarization_prompt)
    llm.save()
    model_selected = LLM_models.objects.get( name = "Llama2" )


@login_required(login_url='login')
def index(request):
    user = request.user
    # try:
    #     current_chat  = request.COOKIES['current_chat']  
    #     print(current_chat,"from cookies")
    # except:
    #     current_chat=0
    
    current_chat = request.session.get('current_chat', 0)
    model = request.session.get('model_selected', 1)
    model_selected = LLM_models.objects.get(id = model)
    history = Chat.objects.filter(user=user)
    chat_history = Transaction.objects.filter(chat=current_chat)
    documents = Documents.objects.filter(chat=current_chat)

    if current_chat!=0:
        current_chat = Chat.objects.get(id=current_chat)
        request.session['current_chat']=current_chat.id
        chat_history = Transaction.objects.filter(chat=current_chat)
    if current_chat == 0:
            response = redirect('index')
            chat=Chat.objects.create(user=user)
            current_chat=chat.id
            print("new chat id", current_chat, chat.id)
            request.session['current_chat']=chat.id
            response.set_cookie('current_chat', chat.id)  

    if request.method == 'GET':
        user = request.user
        deleteChat = request.GET.get("delete")
        chat_id = request.GET.get("chatHistory")
        if deleteChat is not None:
            Chat.objects.filter(id=deleteChat).delete()
            print("chat deleted")
            # return redirect('index')

        # Get the path to the media directory
        media_path = os.path.join(settings.MEDIA_ROOT)
        # current_chat = request.session.get('current_chat', current_chat)
       
        try:
            current_chat = Chat.objects.get(id=chat_id)
            print(current_chat, "chat id got")
            chat_history = Transaction.objects.filter(chat=current_chat)
            documents = Documents.objects.filter(chat=current_chat)
        except: 
            pass
        
    llm_models=LLM_models.objects.all()

    context = {
        "llm_models" : llm_models,
        "chat_id" : current_chat,
        'documents': documents,
        'chat_history': chat_history,
        'history': history,
        'model_selected' : model_selected,
    }

    return render(request, 'index.html', context)   
    

def clear_records(request):
    response = redirect('index')
    user = request.user
    request.session['current_chat'] = 0
    request.session['model_selected'] = 1
    response.set_cookie('current_chat', 0)  
    # Clear all records from the database
    Chat.objects.filter(user=user).delete()
  
    # Clear all files from the media directory
    media_path = os.path.join(settings.MEDIA_ROOT)
    for file in os.listdir(media_path):
        file_path = os.path.join(media_path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    return response


import urllib.parse

def view_file(request, fileName):
    current_chat = request.session.get('current_chat')
    file_name = urllib.parse.unquote(fileName)
    document = Documents.objects.filter(chat=current_chat)
    file_path = os.path.join(settings.MEDIA_ROOT)

    if os.path.exists(file_path):
        context = {
            'filename': file_name,
            'filepath': file_path,  # Use Django's serve view
        }
        return render(request, 'file.html', context)
    else:
        return HttpResponse("File not found", status=404)
    

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            a="Your password and confirm password are not Same!!"
            context= {'a' : a}
            return render(request,'signup.html',context)
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render (request,'signup.html')



def LoginPage(request):
    global current_chat
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            current_chat = 0
            return redirect('index')
        else:
            a='Username or Password is incorrect!!!'
            context={'a': a}
            return render(request, 'login.html',context)
    return render (request,'login.html')


def LogoutPage(request):
    
    logout(request)
    return redirect('login')
    
def getHistory(request):

    user = request.user
    
    history = Chat.objects.filter(user=user)
    
    context ={
        'history': history,
    }
    return render(request,"history.html",context)

def createChat(request):
    response=redirect('index')
    response.set_cookie('current_chat', 0)  
    request.session['current_chat'] = 0
    return response



def model_view(request, model_no):
    model_id = LLM_models.objects.get(id=model_no)
    request.session['model_selected'] = model_id.id
    return redirect('index')

def Upload(request):
    current_chat=request.session.get('current_chat')
    user = request.user
    if request.method == 'POST' and 'file-uploaded' in request.FILES:
        uploaded_file = request.FILES['file-uploaded']
        
        # Save file to media directory
        file_name = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
        if current_chat == 0:
            chat=Chat.objects.create(user=user,title=uploaded_file.name)
        
            request.session['current_chat']=chat.id
            current_chat=request.session['current_chat']

        # Create a record in the database
        file_instance = Documents.objects.create(
            chat_id=current_chat,
            name=uploaded_file.name,
            file_path=file_name
        )
    else:
        pass


    return redirect('index')


def AddModel(request):
    if request.method == 'POST' :
        Name=request.POST.get('name')
        ModelKey=request.POST.get('ModelKey')
        
        path = f"base_models/{Name}"
        llm = LLM_models.objects.create(name=Name, modelKEY = ModelKey, file_path=path)
        llm.save()
        return redirect('index')

    
    return render(request,"AddLLM.html")

def About(request):
    return render(request,'about.html')