from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, error_messages={
        'unique': "A user with that email already exists."})

    #phone = models.CharField(max_length=15, blank=True, null=True)
    #avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    #language = models.CharField(max_length=10, default='pt-br')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.email