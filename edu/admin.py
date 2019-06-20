from django.contrib import admin

# Register your models here.
from edu.models import City,Org,Classes,School,Student

admin.site.register(City)
admin.site.register(Org)
admin.site.register(Classes)
admin.site.register(School)
admin.site.register(Student)