from django.contrib import admin
from .models import Service, Stylist, Appointment, Comment

admin.site.register(Service)
admin.site.register(Stylist)
admin.site.register(Appointment)
admin.site.register(Comment)
