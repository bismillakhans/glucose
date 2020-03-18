import csv

from django.contrib import admin

# Register your models here.
from django.http import HttpResponse

from glucoApp.models import Experiment


class ExperimentModalAdmin(admin.ModelAdmin):
    actions = ["export_as_csv"]


    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

admin.site.register(Experiment, ExperimentModalAdmin)
