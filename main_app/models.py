from django.db import models
from django.urls import reverse

class Cryptid(models.Model):
  name = models.CharField(max_length=100)
  other = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  location = models.CharField(max_length=100)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('cryptids_detail', kwargs={'cryptid_id': self.id})