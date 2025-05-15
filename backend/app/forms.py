from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import login
from django import forms
from .models import *

class SearchForm(forms.Form):
    """Поиск сведений о машине"""
    query = forms.CharField(
        label='Заводской номер машины:',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Например: 0003, 0027'})
    )