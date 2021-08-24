from django.contrib import admin

from .models import Cryptid, Sighting, Evidence, Photo

admin.site.register(Cryptid)
admin.site.register(Sighting)
admin.site.register(Evidence)
admin.site.register(Photo)