from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

TIMESOFDAY = (
  ('A', 'Dawn'),
  ('B', 'Morning'),
  ('C', 'Midday'),
  ('D', 'Afternoon'),
  ('E', 'Dusk'),
  ('F', 'Evening'),
  ('G', 'Midnight')
)

class Evidence(models.Model):
  evidence = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.evidence

  def get_absolute_url(self):
    return reverse('evidence_detail', kwargs={'pk': self.id})

class Cryptid(models.Model):
  name = models.CharField(max_length=100)
  other = models.CharField(max_length=100)
  description = models.TextField(max_length=150)
  location = models.CharField(max_length=150)
  evidence = models.ManyToManyField(Evidence)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('cryptids_detail', kwargs={'cryptid_id': self.id})

  def sighted_today(self):
    return self.sighting_set.filter(date=date.today()).count() >= 0

  class Meta:
    ordering = ['name']

class Sighting(models.Model):
  date = models.DateField('Sighting Date')
  time_of_day = models.CharField(
    'Time of Day',
    max_length=1,
    choices=TIMESOFDAY,
    default=TIMESOFDAY[0][0]
  )
  notes = models.TextField(max_length=150)
  cryptid = models.ForeignKey(Cryptid, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.cryptid} sighting - {self.get_time_of_day_display()}, {self.date}"

  class Meta:
    ordering = ['-date']

class Photo(models.Model):
  url = models.CharField(max_length=250)
  cryptid = models.OneToOneField(Cryptid, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for cryptid_id: {self.cryptid_id} @{self.url}"