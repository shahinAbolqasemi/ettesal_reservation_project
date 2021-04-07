from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import (
    User, Participant, SessionRequest, ParticipantAssignment
)

admin.site.register(User, ModelAdmin)
admin.site.register(SessionRequest)
admin.site.register(Participant)
admin.site.register(ParticipantAssignment)
