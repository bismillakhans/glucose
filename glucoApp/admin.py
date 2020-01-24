from django.contrib import admin

# Register your models here.
from glucoApp.models import Experiment


class ExperimentModalAdmin(admin.ModelAdmin):
    pass


admin.site.register(Experiment, ExperimentModalAdmin)
