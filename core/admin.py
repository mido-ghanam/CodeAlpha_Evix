from django.contrib import admin
from django.apps import apps


# Explicitly register models in the core app with a basic ModelAdmin
app_config = apps.get_app_config('core')
for model in app_config.get_models():
	try:
		fields = [f.name for f in model._meta.fields][:5]
		attrs = {'list_display': tuple(fields)} if fields else {}
		AdminClass = type(f'{model.__name__}Admin', (admin.ModelAdmin,), attrs)
		admin.site.register(model, AdminClass)
	except admin.sites.AlreadyRegistered:
		pass

