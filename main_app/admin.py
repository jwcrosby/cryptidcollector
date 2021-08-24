from django.contrib import admin

from .models import Cryptid, Sighting, Evidence

admin.site.register(Cryptid)
admin.site.register(Sighting)
admin.site.register(Evidence)