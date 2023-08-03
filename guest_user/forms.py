from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django import forms
from django.contrib.auth.models import User

class UserCreationForm(BaseUserCreationForm):
    """
    A modelform that creates a standard Django user.

    Custom implementations must implement :meth:`get_credentials`.

    """  
    class Meta(BaseUserCreationForm.Meta):
        model = User


    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'text-sm:text-base placeholder-gray-500 p-1  pr-4 rounded-lg border border-gray-400 w-full py-2 focus:outline-none focus:border-blue-400',"placeholder":" Enter You Username"}), label="username")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'text-sm:text-base placeholder-gray-500 p-1  pr-4 rounded-lg border border-gray-400 w-full py-2 focus:outline-none focus:border-blue-400',"placeholder":" Enter You Email"}) ,label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-sm:text-base placeholder-gray-500 pl-1 pr-4 rounded-lg border border-gray-400 w-full py-2 focus:outline-none focus:border-blue-400',"placeholder":" Enter You Password"}), label="password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-sm:text-base placeholder-gray-500 pl-1 pr-4 rounded-lg border border-gray-400 w-full py-2 focus:outline-none focus:border-blue-400',"placeholder":" Confirm" ,}), label="confirm password")


    def get_credentials(self) -> dict:
        """
        Get the credentials required to log the user in after conversion.

        The credentials are passed to Django's :func:`authenticate()<django.contrib.auth.authenticate>`.

        :return: Login credentials. This is usually a dict with "username" and "password".

        """
        return {
            "username": self.cleaned_data["username"],
            "password": self.cleaned_data["password1"],
            "email":self.cleaned_data['email'],

        }
