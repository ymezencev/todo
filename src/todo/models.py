from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint


class Category(models.Model):
    name = models.CharField(max_length=30, null=False)
    order_num = models.IntegerField(null=False, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    slug = models.SlugField(max_length=160, null=False,  editable=False)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'slug'], name='unique_user_slug'),
            UniqueConstraint(fields=['user', 'order_num'], name='unique_user_order'),
        ]

    def save(self, *args, **kwargs):
        # setting up default value for order_num
        if not self.order_num:
            self.order_num = self.get_new_order_num()
        super().save()

    def get_new_order_num(self):
        """Auto increment category order_num for every user"""
        last_category = Category.objects.filter(user=self.user).order_by('order_num').last()
        if last_category:
            return last_category.order_num + 1
        return 1

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
