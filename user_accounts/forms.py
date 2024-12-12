# forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):

    #hide usable password options
    usable_password = None

    class Meta:
        model = User
         # Fields from User model to be included in the form
        fields = ['username','email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].widget.attrs['placeholder ']='User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class ="form-text text-muted"><small>Required. 150 characters</span>'

        self.fields['email'].widget.attrs['class']='form-control'
        self.fields['email'].widget.attrs['placeholder ']='Email Address'
        self.fields['email'].label = ''

        self.fields['first_name'].widget.attrs['class']='form-control'
        self.fields['first_name'].widget.attrs['placeholder ']='First Name'
        self.fields['first_name'].label = ''

        self.fields['last_name'].widget.attrs['class']='form-control'
        self.fields['last_name'].widget.attrs['placeholder ']='Last Name'
        self.fields['last_name'].label = ''
