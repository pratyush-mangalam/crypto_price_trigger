from django.db import models

from crypto_price_trigger.users.models import Users


class Alert(models.Model):
    DAYS_OF_THE_WEEK = (
        ("Created", "Created"),
        ("Deleted", "Deleted"),
        ("Triggered", "Triggered"),
    )
    stock_id = models.CharField(max_length=100, null=False, blank=False)
    stock_name = models.CharField(max_length=100, null=False, blank=False)
    stock_price = models.IntegerField(null=False, blank=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, blank=False)
    alert_sent = models.BooleanField(default=False, null=False, blank=False)
    status = models.CharField(choices=DAYS_OF_THE_WEEK, default="Created", max_length=15)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stock_id

    class Meta:
        db_table = "alert"
