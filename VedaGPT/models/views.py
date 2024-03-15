# views.py

from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import default_storage

from .privatellm import Laama,Geema
from .privatellm import IfPdf
from .models import Chat,Transaction
import os
import mimetypes

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

current_chat=0
model = "Laama"


def index(request):
    
    global current_chat
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
    if request.method == 'GET' and current_chat != 0 :
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
    # documents = [{'name': f, 'url': default_storage.url(f)} for f in os.listdir(media_path) if os.path.isfile(os.path.join(media_path, f))]

    
    context = {
        # 'documents': documents,
        'chat_history': chat_history,
        'history': history,
        'model' : model,
    }
    return render(request, 'index.html', context)

def send(request):
    global current_chat  # Declare current_chat as global

    user = request.user
    
    if request.method=='POST':
        prompt = request.POST['message']
        file = request.FILES.get('file')

        if current_chat == 0:
            chat=Chat.objects.create(user=user,title=prompt[:15])
            current_chat=chat
            print(current_chat,"chat id created")
    

    filename = file.name if file else None

    if file:
     
        file_path = default_storage.save(filename, file)
        file_url = default_storage.url(file_path)

  
        context = IfPdf.context(os.path.join(settings.MEDIA_ROOT, filename), prompt)
        print("pdf Reply")
        # reply = Promt_reply.replyPdf(prompt, context)
        if model == "Laama":
            reply=Laama.replyPdf(prompt, context)
        # if model == "Gamma":
        else:
            reply=Geema.replyPdf(prompt, context)
        transaction_instance = Transaction.objects.create(chat=current_chat, input_prompt=prompt, output=reply)
    else:
        # Generate a reply based on the prompt
        # reply = Promt_reply.reply(prompt)
        print("message reply")
        if model == "Laama":
            reply=Laama.reply(prompt)
        # if model == "Gamma":
        else:
            reply=Geema.reply(prompt)
        
        transaction_instance = Transaction.objects.create(chat=current_chat, input_prompt=prompt, output=reply)
    
    # Save chat history
    transaction_instance.save()

    context = {
        'reply': reply,
        'filename': filename,
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


def viewFile(request, fileName):
    file_path = os.path.join(settings.MEDIA_ROOT, fileName)

    if os.path.exists(file_path):
        context = {
            'filename': fileName,
            'filepath': file_path,
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


def model(request,model_no):
    global model
    if model_no == 1 :
        model = "Laama"
    if model_no == 2 :
        model = "Geema"
    return redirect('index')

