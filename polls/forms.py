from django import forms
from .models import Question,Users
import collections
import datetime
from django.contrib import auth
from django.contrib.auth.models import User
class DetailForm(forms.Form):
    def __init__(self,q_id,*args,**kwargs):
        super(DetailForm,self).__init__(*args,**kwargs)
        self.question=Question.objects.get(pk=q_id)
        self.fields['choice_field'] = forms.ChoiceField(label='',widget=forms.RadioSelect, choices=self.func())


    def func(self):
        choice_list_of_tuples=[]
        choices=self.question.choice_set.all()
        for index,data in enumerate(choices):
            choice_list_of_tuples.append((index+1,data.choice_text))
        return tuple(choice_list_of_tuples)    

class Signup(forms.Form):
    fullName=forms.CharField(label="Username",max_length=20)
    password=forms.CharField(label="Password",max_length=14)
    dateOfBirth=forms.DateField(label="Date of Birth")

    def person_save(self):
        user=User.objects.create_user(username=self.cleaned_data['fullName'],
                                      password=self.cleaned_data['password'],
                                      date_joined=self.cleaned_data['dateOfBirth'])
        user.save()
        return user

class Login(forms.Form):
    user_name=forms.CharField(label="Your name",max_length=20)
    password=forms.CharField(label="Password",max_length=14)

    def person_validate(self):
        user=auth.authenticate(username=self.cleaned_data['user_name'],
                               password=self.cleaned_data['password'])
        if user is not None and user.is_active:
            return user
        return False     



