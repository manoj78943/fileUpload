# file_upload_app/forms.py
from django import forms
from django.contrib.auth.models import User

class FileUploadForm(forms.Form):
    file = forms.FileField()

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
