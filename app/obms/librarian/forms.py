from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Reader, Book

class ReaderForm(ModelForm):
    confirmPassword = forms.CharField(widget=forms.PasswordInput(), validators=[validate_password], label="Confirm Password")
    class Meta:
        model = Reader
        fields = ['confirmPassword', 'favoriteBook', 'favoriteAuthor', 'favoriteGenre']

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), validators=[validate_password])
    class Meta:
        model = User
        fields = ['username', 'password']

class ProfileForm(ModelForm):
    class Meta:
        model = Reader
        fields = ['username', 'favoriteBook', 'favoriteAuthor', 'favoriteGenre']

class BookForm(ModelForm):
    id = forms.IntegerField()
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'checkedOut']
