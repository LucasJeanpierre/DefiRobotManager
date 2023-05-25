from django.contrib import admin
from .models import Institution, AesteticScores, Team, Run
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class InstitutionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'id')
    
class AesteticScoresAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('institution', 'first_rank', 'second_rank', 'third_rank')
    list_filter = ('institution', 'first_rank', 'second_rank', 'third_rank')

class TeamAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'institution', 'order')
    list_filter = ('name', 'institution', 'order')

class RunAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = ('num_run', 'team', 'time', 'score',)
    list_display = ('team', 'time', 'score', 'num_run')
    list_filter = ('team', 'time', 'score', 'num_run')
    ordering = ('-score', '-time', '-num_run')

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(AesteticScores, AesteticScoresAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Run, RunAdmin)
