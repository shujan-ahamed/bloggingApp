from django import forms
from django.forms import ModelForm
from .models import Post, Comment, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from ckeditor_uploader.widgets import CKEditorUploadingWidget






class RegistrationForm(UserCreationForm):
    model = User
    
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control','id':'form3Example1c'}))
    first_name = forms.CharField(max_length=30, required=False, help_text='Option',widget=forms.TextInput(attrs={'class': 'form-control','id':'form3Example1c'}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Option',widget=forms.TextInput(attrs={'class': 'form-control','id':'form3Example3c'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','id':'form3Example3c'}))
    password1 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class': 'form-control','id':'form3Example4c'}))
    password2 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class': 'form-control','id':'form3Example4c'}))

    fields= ['username','first_name','last_name','email','password1','password2']

class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, category):
        return category.name
    

class PostForm(ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    
    class Meta:
        
        model = Post
        fields = ['title','category', 'text']

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }
    # save_button = forms.SubmitButton(
    #     label='Save',
    #     widget=forms.widgets.Submit(attrs={'class': 'btn btn-primary'}),
    #     type='submit'
    # )

    # publish_button = forms.Button(
    #     label='Publish',
    #     widget=forms.widgets.Button(attrs={'class': 'btn btn-success'}),
    #     type='button'
    # )
    


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control editable medium-editor-textarea postcontent', 'placeholder':'Add comment'}),
        }

class PostSearchForm(forms.Form):
    q = forms.CharField()
    c= forms.ModelChoiceField(
        queryset = Category.objects.all().order_by('name')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['c'].label = ''
        self.fields['c'].required = False
        self.fields['q'].help_text = 'search for.'
        self.fields['c'].label = 'category'
        self.fields['q'].widget.attrs.update(
            {'class' : 'form-control'}
        )