from django.contrib import admin

# Register your models here.

from .models import Institution, AesteticScores, Team, Run

admin.site.register(Institution)
admin.site.register(AesteticScores)
admin.site.register(Team)
admin.site.register(Run)
