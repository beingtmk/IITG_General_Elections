from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.apps import apps

# app =
class VoterListResource(resources.ModelResource):
	class Meta:
		model = VoterList
		skip_unchanged = True
		report_skipped = True
		import_id_fields = ['webmail_id']

class VoterListAdmin(ImportExportModelAdmin):
	resource_class = VoterListResource
	search_fields = ('webmail_id','roll_no','name')

admin.site.register(VoterList, VoterListAdmin)


class ContestantsResource(resources.ModelResource):
	class Meta:
		model = Contestants
		skip_unchanged = True
		report_skipped = True
		import_id_fields = ['webmail_id']

class ContestantsAdmin(ImportExportModelAdmin):
	resource_class = VoterListResource
	search_fields = ('webmail_id','name')

admin.site.register(Contestants, ContestantsAdmin)
admin.site.register(Admin)

