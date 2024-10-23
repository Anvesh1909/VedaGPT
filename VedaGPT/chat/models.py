from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=True)
   
    def __str__(self):
        return str(self.id)



class Transaction(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    input_prompt = models.CharField(max_length=255)
    output = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.input_prompt


class Documents(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)


class LLM_models(models.Model):
    name = models.CharField(max_length=100)
    modelKEY = models.CharField(max_length=100)
    file_path = models.CharField(max_length=100)
    prompt = models.TextField(default = "")
    pdf_prompt= models.TextField(default="")
    summarization_prompt = models.TextField(default="")

    def __str__(self):
        return self.name
