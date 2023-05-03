from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=249, null=False, blank=False, unique=True)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=249, blank=False, null=False)
    objects = models.Manager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"
