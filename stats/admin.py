from django.contrib import admin

# Register your models here.

from .models import Institution, AesteticScores, Team, Run


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    
class AesteticScoresAdmin(admin.ModelAdmin):
    list_display = ('institution', 'first_rank', 'second_rank', 'third_rank')
    list_filter = ('institution', 'first_rank', 'second_rank', 'third_rank')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution')
    list_filter = ('name', 'institution')

class RunAdmin(admin.ModelAdmin):
    fields = ('num_run', 'team', 'time', 'score',)
    list_display = ('team', 'time', 'score', 'num_run')
    list_filter = ('team', 'time', 'score', 'num_run')
    ordering = ('-score', '-time', '-num_run')

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(AesteticScores, AesteticScoresAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Run, RunAdmin)
