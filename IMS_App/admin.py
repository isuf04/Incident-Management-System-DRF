from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Users)
admin.site.register(Employee)
admin.site.register(Incident_Ticket)
admin.site.register(Incident_type)
admin.site.register(Incident_Status)
admin.site.register(Status)
admin.site.register(Role)
admin.site.register(Stack_Holder)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Department_poc)
admin.site.register(Contributing_Factor)
admin.site.register(Followup_Action)
admin.site.register(Immediate_Action)
admin.site.register(Improvement_Recommendation)
admin.site.register(Document)
