from django.db import models
from django.urls import reverse

TIMESOFDAY = (
  ('A', 'Dawn'),
  ('B', 'Morning'),
  ('C', 'Midday'),
  ('D', 'Afternoon'),
  ('E', 'Dusk'),
  ('F', 'Evening'),
  ('G', 'Midnight')
)

class Cryptid(models.Model):
  name = models.CharField(max_length=100)
  other = models.CharField(max_length=100)
  description = models.TextField(max_length=150)
  location = models.CharField(max_length=150)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('cryptids_detail', kwargs={'cryptid_id': self.id})

class Sighting(models.Model):
  date = models.DateField()
  time_of_day = models.CharField(
    max_length=1,
    choices=TIMESOFDAY,
    default=TIMESOFDAY[0][0]
  )
  notes = models.TextField(max_length=150)
  cryptid = models.ForeignKey(Cryptid, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.get_time_of_day_display()} on {self.date}"