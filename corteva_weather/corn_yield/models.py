from django.db import models

# Create your models here.


class CornYieldModel(models.Model):
    year = models.SmallIntegerField(unique=True, null=False)
    corn_yield = models.IntegerField(null=False)
