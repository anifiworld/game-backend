# Create your models here.
from django.db import models
from django.utils import timezone

# Create your models here.


class Color(models.Model):
    name = models.CharField(max_length=20, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Fruit(models.Model):
    name = models.CharField(max_length=30, unique=True)
    # color = models.CharField(max_length=20)
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, related_name="fruits", blank=True, null=True
    )
    extinct_at = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
