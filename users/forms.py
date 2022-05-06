
from django.forms import ModelForm
from django import forms
from django.contrib.auth import (password_validation,)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import User


class CreateUserForm(UserCreationForm):

    error_messages = {
        'password_mismatch': 'Las contraseñas no coinciden.',
    }

    username = UsernameField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'autocomplete': 'none','placeholder': 'Usuario'}),
        min_length=5,
        error_messages={'unique': 'Ya existe un usuario con este nombre.', 'min_length': 'El nombre debe tener al menos 5 caracteres.', 'max_length': 'El nombre debe tener menos de 16 caracteres.'},
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autocomplete': 'new-email','placeholder': 'Email'}),
        error_messages={'unique': 'Ya existe un usuario con este email.'},
    )

    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Contraseña'}),
    )
    password2 = forms.CharField(
        label="Confirme la contraseña",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirma la contraseña'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ("username","email", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class EditBookInList(forms.Form):
    pass


class AddBookToList(forms.Form):
    pass
