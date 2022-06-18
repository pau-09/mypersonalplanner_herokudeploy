from django.forms import Form
from django import forms
from django.contrib.auth import (
    password_validation,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UsernameField
from books.models import Book
from movies.models import Movie
from .models import User


class CreateUserForm(UserCreationForm):

    error_messages = {
        "password_mismatch": "Las contraseñas no coinciden.",
    }

    username = UsernameField(
        label="Nombre de usuario",
        widget=forms.TextInput(
            attrs={"autocomplete": "none", "placeholder": "Usuario"}
        ),
        min_length=5,
        error_messages={
            "unique": "Ya existe un usuario con este nombre.",
            "min_length": "El nombre debe tener al menos 5 caracteres.",
            "max_length": "El nombre debe tener menos de 16 caracteres.",
        },
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"autocomplete": "new-email", "placeholder": "Email"}
        ),
        error_messages={"unique": "Ya existe un usuario con este email."},
    )

    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "Contraseña"}
        ),
    )
    password2 = forms.CharField(
        label="Confirme la contraseña",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Confirma la contraseña",
            }
        ),
        strip=False,
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AddEntryForm(Form):
    ENTRY_TYPE_CHOICES = [("Book", "Libro"), ("Movie", "Película")]

    type = forms.ChoiceField(
        choices=ENTRY_TYPE_CHOICES,
    )

    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Título"}),
        error_messages={"unique": "Ya existe una entrada con este titulo."},
    )

    author_or_director = forms.CharField(
        initial="Anónimo",
    )

    year = forms.IntegerField(min_value=1000, max_value=9999, error_messages="")

    book_genre = forms.ChoiceField(
        choices=Book.GENRES,
        required=False,
    )

    movie_genre = forms.ChoiceField(
        choices=Movie.GENRES,
        required=False,
    )

    def validate_is_unique(self):
        if self.data["type"] == "Book":
            model = Book
        elif self.data["type"] == "Movie":
            model = Movie

        try:
            entry = model.objects.get(title=self.data["title"])
            self.valid = False if entry else True
        except model.DoesNotExist:
            self.valid = True

    def save(self):

        self.full_clean()
        self.validate_is_unique()

        if self.valid:
            if self.data["type"] == "Book":
                entry = Book.objects.create(
                    title=self.data["title"],
                    author=self.data["author_or_director"],
                    year=self.data["year"],
                    genre=self.data["book_genre"],
                )

            elif self.data["type"] == "Movie":
                entry = Movie.objects.create(
                    title=self.data["title"],
                    director=self.data["author_or_director"],
                    year=self.data["year"],
                    genre=self.data["movie_genre"],
                )

        else:
            self.errors["unique"] = "Ya existe una entrada con este título."

        if not self.errors and entry:
            return (
                f"La entrada para '{entry.title}' ha sido creada correctamente."
            )
        else:
            return ""
