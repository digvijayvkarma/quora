from cProfile import label
from django import forms
from .models import *

class QuestionForm(forms.Form):
    question = forms.CharField(label= 'Question ', max_length = 200)

class AnswerForm(forms.Form):
    answer = forms.CharField(label= 'Your Answer ', max_length = 200)

class LoginForm(forms.Form):
    login_id = forms.EmailField(label= 'login_id')
    password = forms.CharField(label= 'Password', max_length = 20)

class SignUpForm(forms.Form):
    login_id = forms.EmailField(label= 'Username')
    firstName = forms.CharField(label= 'First Name', max_length = 50)
    lastName = forms.CharField(label= 'Last Name', max_length = 50)
    password = forms.CharField(label= 'Password', max_length = 20)
    