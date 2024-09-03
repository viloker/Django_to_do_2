from django.db import models


class UserModel(models.Model):
    objects = models.Manager()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.email


class TasksModels(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='tasks')
    task = models.CharField(max_length=128)

    def __str__(self):
        return self.task
