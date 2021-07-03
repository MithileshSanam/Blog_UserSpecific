from blogapp.models import Post
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
class PostForm(forms.ModelForm):
    class Meta:
        fields = ('title','text')
        model = Post
        widgets = {
        'title': forms.TextInput(attrs={'class':'form-control','id':'fortitle'}),
        'text': forms.Textarea(attrs={'class':'form-control','id':'fortext'}),
        }
