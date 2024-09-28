from django.contrib import admin
import django.apps
class E_approval_admin(admin.AdminSite):
    site_header='RIT-EAPPROVAL ADMIN'
admin_site=E_approval_admin(name='RIT Admin')
models=django.apps.apps.get_models()
for model in models:
    try:
        admin_site.register(model)
    except:
        print("model not found")
