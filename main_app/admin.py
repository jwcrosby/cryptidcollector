from django.contrib import admin

from .models import Cryptid, Sighting

admin.site.register(Cryptid)
admin.site.register(Sighting)