from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    patronymic = models.CharField('Отчество', max_length=150, blank=True)
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.last_name} {self.first_name}" if self.first_name else self.username