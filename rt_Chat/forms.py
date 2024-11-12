from django.forms import ModelForm
from .models import *
from django import forms

class AddMessage(ModelForm):
    class Meta:
        model = GroupMessages
        fields = ['body',]
        widgets = {
        'body' : forms.TextInput(attrs = {'placeholder' : 'Add message ...' , 'class' : 'p-4 text-black' , 'maxlength' : 300 , 'autofocus' : True}),
        }
        
class NewGroupForm(ModelForm):
    class Meta:
        model = GroupName
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name' : forms.TextInput(attrs={
                'placeholder': 'Add name ...', 
                'class': 'p-4 text-black', 
                'maxlength' : '300', 
                'autofocus': True,
                }),
        }

class ChatRoomEditForm(ModelForm):
    class Meta:
        model = GroupName
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name' : forms.TextInput(attrs={
                'class': 'p-4 text-xl font-bold mb-4', 
                'maxlength' : '300', 
                }),
        }