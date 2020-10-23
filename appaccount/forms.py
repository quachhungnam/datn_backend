# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from appaccount.models import User as CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email','is_teacher','birthday')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email','is_teacher','birthday')


# class BroadcastForm(forms.Form):
#     _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
#     broadcast_text = forms.CharField(widget=forms.Textarea)
#     bot = forms.ModelChoiceField(Bot.objects)