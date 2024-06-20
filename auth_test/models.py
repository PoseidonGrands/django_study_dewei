from django.db import models

# Create your models here.
class APage(models.Model):
    title = models.CharField(max_length=64)
    class Meta:
        permissions = [('look_a_page', 'can get a page')]


class BPage(models.Model):
    title = models.CharField(max_length=64)
    class Meta:
        permissions = [('look_b_page', 'can get b page')]


