

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=True)
   
    def __str__(self):
        return self.title

class Documents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doc_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.doc_name

class Transaction(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    doc = models.ForeignKey('Documents', on_delete=models.SET_NULL, null=True)
    input_prompt = models.CharField(max_length=255)
    output = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.input_prompt


