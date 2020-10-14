from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, null=False)
    order_num = models.IntegerField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    url = models.CharField(max_length=256, default=hash(id), null=False, editable=False)

    def __str__(self):
        return f'[{self.order_num}] {self.name}'


class Task(models.Model):
    task = models.CharField(max_length=400, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_important = models.BooleanField(default=False, null=False)
    is_completed = models.BooleanField(default=False, null=False)
    date_completed = models.DateTimeField(null=True)
    category = models.ManyToManyField(Category)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.task}'
