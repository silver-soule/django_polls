from django import forms
from .models import Question,Users
import collections
import datetime
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
    fullName=forms.CharField(label="Your name",max_length=20)
    number=forms.CharField(label="Phone Number",max_length=14)
    dateOfBirth=forms.DateField(label="Date of Birth")

    def person_save(self):
        person=Users(username=self.cleaned_data['fullName'],
                    phone_number=self.cleaned_data['number'],
                    date_of_birth=self.cleaned_data['dateOfBirth'])
        person.save()
        return person





