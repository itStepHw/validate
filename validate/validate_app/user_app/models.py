# models.py
from django.db import models
from django.core.exceptions import ValidationError
import re


def validate_username(username):
    if len(username) < 3:
        raise ValidationError('Имя пользователя должно содержать не менее 3 символов.')


def validate_email(email):
    if 'spam' in email:
        raise ValidationError('Адрес электронной почты не должен содержать слово "spam".')


def validate_passwords(password, confirm_password):
    if password != confirm_password:
        raise ValidationError('Пароль и подтверждение пароля не совпадают.')


def validate_strong_password(password):
    if len(password) < 8:
        raise ValidationError('Пароль должен содержать не менее 8 символов.')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Пароль должен содержать хотя бы одну строчную букву.')
    if not re.search(r'\d', password):
        raise ValidationError('Пароль должен содержать хотя бы одну цифру.')
    if not re.search(r'\W', password):
        raise ValidationError('Пароль должен содержать хотя бы один специальный символ.')


class User(models.Model):
    username = models.CharField(max_length=150, unique=True, validators=[validate_username])
    email = models.EmailField(unique=True, validators=[validate_email])
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)

    def clean(self):
        validate_passwords(self.password, self.confirm_password)
        validate_strong_password(self.password)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
