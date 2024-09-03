from django import forms

#log in
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=16 ,widget=forms.PasswordInput)

# task (main)
class TasksForm(forms.Form):
    task = forms.CharField(max_length=128)