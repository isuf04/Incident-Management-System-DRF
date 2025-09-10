from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('employees', views.EmployeeView),
    path('role/', views.Role_View),
    path('user', views.UsersView),
    path('incident_type' , views.incident_type),
    path('status' , views.Statusview),
    path('incident_ticket' , views.Incident_ticket),
    path('incident_status' , views.incident_Status),
    path("designation", views.Designation_View),
    path('departments' , views.Department_View),
    path('stackholder' , views.Stackholder_view),
    path('departmentpoc' , views.DepartmentPoc_View),
    path('contributing_fact' , views.Contributing_factor_View),
    path("improvement/", views.improvement_recommendation_api),  
    path("followup", views.followup_action_api),  
    path("immediate", views.immediate_action_api), 
    path('upload' ,views.document_upload_view)
    
]























# + static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
