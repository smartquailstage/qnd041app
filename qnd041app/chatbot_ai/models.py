from django.db import models

class CompanyInfo(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    active = models.BooleanField(default=True)


class PendingAppointment(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    desired_date = models.DateTimeField(blank=True, null=True)
    step = models.IntegerField(default=1)  # 1=pedir nombre, 2=pedir fecha, 3=cita creada
