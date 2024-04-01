# views.py

from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .privatellm import IfPdf,llm
from .models import Chat,Transaction,Documents,LLM_models
import os
import mimetypes

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


models = {
    "1" : "Laama",
    "2" : "Gemma",
}

current_chat=0
model_selected = LLM_models.objects.get( name = "Laama" ) #default first model

filesUploaded = []


@login_required(login_url='login')
def index(request):

    global current_chat,model_selected
    user = request.user
    # remove this if we want only users can access this website
    if not user.is_authenticated:
        user=authenticate(request,username='Anonymous',password="1234")
        if user is not None:
            login(request,user)
            current_chat = 0
            return redirect('index')
        else:
            a='Username or Password is incorrect!!!'
            context={'a': a}
            return render(request, 'login.html',context)

    context = {

    }
    history = Chat.objects.filter(user=user)
    chat_history = Transaction.objects.filter(chat=current_chat)


    if request.method == 'GET':
        user = request.user
        deleteChat = request.GET.get("delete")
        if deleteChat is not None:
            Chat.objects.filter(id=deleteChat).delete()
            return redirect('index')

        # Get the path to the media directory
        media_path = os.path.join(settings.MEDIA_ROOT)
        print(request.GET.get("chatHistory"),12345678)
        chat_id = request.GET.get("chatHistory")
        print(chat_id, "hello world") 
        try:
            current_chat = Chat.objects.get(id=chat_id)
            print(current_chat, "hello world")
            chat_history = Transaction.objects.filter(chat=current_chat)
        except Chat.DoesNotExist:
            pass
    
    # Collect information about available documents
    documents = Documents.objects.filter(chat=current_chat)
    llm_models=LLM_models.objects.all()

    context = {
        "llm_models" : llm_models,
        "current_chat" : current_chat,
        'documents': documents,
        'chat_history': chat_history,
        'history': history,
        'model_selected' : model_selected.name,
    }
    return render(request, 'index.html', context)

def send(request):
    global current_chat  # Declare current_chat as global

    user = request.user
    
    if request.method=='POST':
        User_prompt = request.POST['message']
        if current_chat == 0:
            chat=Chat.objects.create(user=user,title=User_prompt[:15])
            current_chat=chat
            print(current_chat,"chat id created")
    
    documents = Documents.objects.filter(chat=current_chat)

    if documents:
        for document in documents:
            file_path = os.path.join(settings.MEDIA_ROOT, document.file_path)
            context = IfPdf.context(file_path, User_prompt)

            print("pdf Reply")

            reply=llm.LLM_reply( User_prompt, context = context, Model_id = model_selected.id  )
            
            transaction_instance = Transaction.objects.create(chat=current_chat, input_prompt=User_prompt, output=reply)
    else:
        
        print("message reply")
        
        reply=llm.LLM_reply( User_prompt ,  Model_id = model_selected.id )
        
        
        transaction_instance = Transaction.objects.create(chat=current_chat, input_prompt = User_prompt, output=reply)
    
    # Save chat history
    transaction_instance.save()

    context = {
        'reply': reply,
        # 'filename': document.file_path,
    }

    return JsonResponse(context)

def clear_records(request):
    global current_chat
    current_chat = 0
    user = request.user

    # Clear all records from the database
    Chat.objects.filter(user=user).delete()
    print("chat history deleated")
    # Clear all files from the media directory
    media_path = os.path.join(settings.MEDIA_ROOT)
    for file in os.listdir(media_path):
        file_path = os.path.join(media_path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    return redirect('index')

from django.contrib.staticfiles.views import serve


import urllib.parse

def view_file(request, fileName):
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
    if request.method=='POST':
        pass
    global current_chat
    current_chat = 0
    return redirect('index')


def model_view(request, model_no):
    global model_selected
    
    model_id = LLM_models.objects.get(id = model_no)
    model_selected = model_id
    print(f"model selected { model_selected}")
    return redirect('index')

def Upload(request):
    global current_chat
    user = request.user
    if request.method == 'POST' and 'file-uploaded' in request.FILES:
        uploaded_file = request.FILES['file-uploaded']
        
        # Save file to media directory
        file_name = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
        if current_chat == 0:
            chat=Chat.objects.create(user=user,title=uploaded_file.name)
            current_chat=chat
            print(current_chat,"chat id created in file uploaded")

        # Create a record in the database
        file_instance = Documents.objects.create(
            chat=current_chat,
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
        print(request.POST)
        path = f"{Name}/base_models"
        llm = LLM_models.objects.create(name=Name, modelKEY = ModelKey, file_path=path)
        llm.save()
        print(LLM_models.objects.all())
        return redirect('index')

    
    return render(request,"AddLLM.html")