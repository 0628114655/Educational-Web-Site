from typing import Any
from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import *

User = get_user_model()


class SearchForm(forms.Form):
    query = forms.CharField(max_length=30)

class UserRegistrationForm(forms.ModelForm):
    choices = [(choice, choice) for choice in ['','TCLSHF-1', 'TCLSHF-2', 'TCLSHF-3', 'TCLSHF-4','TCLSHF-5', 'TCLSHF-6', 'TCSF-1','TCSF-2', 'TCSF-3', 'TCSF-4', 'TCSF-5', '1BLSHF-1', '1BLSHF-2', '1BSEF-1', '1BSEF-2', '2BSHF-1', '2BSEF-2', '2BSVT-1', '2BSPF-1', '2BSPF-2' ]]
    firstname = forms.CharField( label= ' الاسم الشخصي' ,widget=forms.TextInput(attrs={'class': 'form-control',}))
    lastname = forms.CharField( label= ' الاسم العائلي' ,widget=forms.TextInput(attrs={'class': 'form-control',}))
    email = forms.EmailField( label= 'البريد الإلكتروني', widget=forms.EmailInput(attrs={'class': 'form-control', }))
    password = forms.CharField( label= 'كلمة المرور', widget=forms.PasswordInput(attrs={'class': 'form-control', }))
    password_confirmation = forms.CharField( label= 'تأكيد كلمة المرور', widget=forms.PasswordInput(attrs={'class': 'form-control', }))
    section = forms.ChoiceField( label= 'القسم',choices=choices , widget=forms.Select(attrs={'class': 'form-control', }))
    username = forms.CharField( label= 'رقم مسار', widget=forms.TextInput(attrs={'class': 'form-control', }))
    image = forms.ImageField( label= 'الصورة الشخصية', widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email','password','password_confirmation','section','username', 'image']
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        username_error = User.objects.filter(username = username)
        if username_error.exists():
            raise forms.ValidationError('هذا الرمز موجود مسبقا.')

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        check_email =  User.objects.filter(email = email)
        if password != password_confirmation:
            raise forms.ValidationError('كلمتا المرور لا تتطابقان!')
        if check_email.exists():
            raise forms.ValidationError ('هذا البريد الإلكتروني موجود مسبقا.')
        return super(UserRegistrationForm, self).clean(*args, **kwargs)

class UserLoginForm(forms.Form):
    username = forms.CharField( label= 'رقم مسار', widget=forms.TextInput(attrs={'class': 'form-control', }))
    password = forms.CharField(label = 'كلمة المرور', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user =  authenticate(password = password, username = username)
            if not user:
                raise forms.ValidationError(' رمز مسار أو كلمة المرور غير صحيحة.')
            return super(UserLoginForm, self).clean(*args, **kwargs)
