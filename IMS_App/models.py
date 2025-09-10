from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


# Create your models here.




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(("The Email must valid"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)                                      
        extra_fields.setdefault("is_superuser", True)                              
        extra_fields.setdefault("is_active", True)                                    

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)




class Role(models.Model):
    id = models.AutoField(primary_key = True)
    Name = models.CharField(max_length = 100)
    
    def __str__(self):
        return f"{self.Name}"


class Users(AbstractUser ):
    id = models.AutoField(primary_key=True)
    username= None
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role , on_delete=models.CASCADE,null=True)
    is_active = models.BooleanField(default=True)              
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []       
    
    def __str__(self):
        return self.email
    objects = CustomUserManager()


# # {
#   "email": "testuser@example.com",
#   "password": "StrongPassword123",
#   "first_name": "Yusuf",
#   "last_name": "Ali",
#   "role": 1 ,
# "employee" :     {
#       "designation_id": 2 ,
#       "job_title": "Backend Developer",
#       "phone_no": "9876543210"
#     }
# }
    
class Stack_Holder(models.Model):
    id = models.AutoField(primary_key= True)
    user_id = models.OneToOneField(Users , on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user_id.email}"

class Department(models.Model):
    id = models.AutoField(primary_key=True)   
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
    
class Designation(models.Model):
    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length= 50)
    dep_id =models.ForeignKey(Department ,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} ({self.dep_id.name})"

class Employee(models.Model):
    
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(Users , on_delete=models.CASCADE)
    designation_id = models.ForeignKey(Designation , on_delete=models.CASCADE )      
    job_title = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.user_id} - {self.designation_id}"
    # {
    #   "designation": "Software Engineer",
    #   "job_title": "Backend Developer",
    #   "phone_no": "9876543210"
    # }
    
class Department_poc(models.Model):
    id = models.AutoField(primary_key= True)
    department_id = models.ForeignKey(Department , on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.department_id}"

    # {
    #     "department_id": 3,
    #     "employee_id": 7
    # }
    
class Incident_type(models.Model):
    id = models.AutoField(primary_key=True)
    incident_type_Name = models.CharField(max_length=50) 
    department_id=models.ForeignKey(Department , on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.incident_type_Name} - {self.department_id}" 
# {
#     "incident_type_Name": "Network Issue",
#     "department_id": 2
# }


class Incident_Status(models.Model):
    id = models.AutoField(primary_key=True)
    status_id = models.ForeignKey("Status" , on_delete=models.CASCADE)
    date_created = models.DateField(default= timezone.now)
    incident_id = models.ForeignKey("Incident_Ticket", on_delete=models.CASCADE , null=True, blank=True)

    
    def __str__(self):
        return f"Status {self.status_id} - {self.date_created}"
    
#     {
#     "status_id": 1,
#     "date_created": "2025-08-14",
#     "incident_id": [
#         1
#     ]
# }

    
class Status(models.Model):
    id = models.IntegerField(primary_key=True)
    status_name = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.status_name}"
    
    
# {
#     "incident_status": 1,
#     "name": "Open"
# }   
    

class Contributing_Factor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name}"


class Improvement_Recommendation(models.Model):
    id = models.AutoField(primary_key = True)
    action = models.CharField(max_length = 700, null = True)
    action_description=models.CharField(max_length=100)
    responsible_employee_id = models.ForeignKey("Employee", on_delete = models.CASCADE ,  related_name="improvement_tasks")
    incidentid = models.ForeignKey("Incident_ticket", on_delete = models.CASCADE)
    
    def __str__(self):
        return f"{self.responsible_employee_id}"
    

class Followup_Action(models.Model):
    id = models.AutoField(primary_key = True)
    action_title = models.CharField(max_length = 1000, null = True)
    date_completed= models.DateField(default=timezone.now)
    action_description = models.CharField(max_length=100)
    responsible_employee = models.ForeignKey("Employee", on_delete = models.CASCADE )
    incidentid = models.ForeignKey("Incident_ticket", on_delete = models.CASCADE)
    def __str__(self):
        return f"{self.responsible_employee}"
        

class Immediate_Action(models.Model):
    id = models.AutoField(primary_key = True)
    title= models.CharField(max_length=200 )
    description=models.CharField(max_length=100)
    employeeid = models.ForeignKey("Employee" , on_delete = models.CASCADE)
    incidentid = models.ForeignKey("Incident_ticket", on_delete = models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.employeeid}"
    
        
class Incident_Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    assinged_poc= models.ForeignKey("Department_poc" , on_delete=models.CASCADE )
    requestor_id = models.ForeignKey("Employee" , on_delete=models.CASCADE)
    report_type = models.ForeignKey("Incident_type",on_delete=models.CASCADE) 
    occurrence_date = models.DateField(default=timezone.now)
    location = models.CharField(max_length= 40 , null=True)
    departments= models.ForeignKey("Department" , on_delete=models.CASCADE)
    risk_level =models.CharField(max_length=100 , null=True)
    contributing_factor = models.ManyToManyField('Contributing_Factor')
    facility = models.CharField(max_length=50 , null=True)
    description = models.TextField(max_length=50 , null=True)
    recurrence = models.CharField(max_length=100 , null=True)
    potential_severity = models.CharField(max_length=100 , null=True)
    improvementrecommendation = models.ManyToManyField("Employee", through = "Improvement_Recommendation", related_name="incident_improvement_recommendation")
    followupactions = models.ManyToManyField("Employee", through = "Followup_Action", related_name="incident_followup_action")
    immediateaction = models.ManyToManyField("Employee" , through="Immediate_Action" ,related_name="incident_immidiate_action")
    individualsinvolved = models.ManyToManyField("Employee", db_table = "Individuals_involved", null=True, related_name="Incident_individuals")
    incidentwitnesses = models.ManyToManyField("Employee", db_table = "Incident_witness", null=True, related_name="Incident_Witnesses")
    incidentfactors = models.ManyToManyField("Employee" , db_table="Incident_factor",null=True , related_name="Incident_factor")
    file=models.FileField(upload_to="uploads/" , null=True , blank=True)
    
    def __str__(self):
        return f"{self.assinged_poc} - {self.requestor_id}"


#Payload
# {
#     "department": 1,
#     "requestor": 2,
#     "report_type": 1,
#     "occurrence_date": "2025-08-19",
#     "location": "Delhi Office",
#     "risk_level": "High",
#     "facility": "Main Building",
#     "description": "System outage caused transaction delays",
#     "recurrence": "No",
#     "potential_severity": "Major",

#     "contributing_factors": [1, 3],
#     "individuals_involved": [2, 4],
#     "incident_witnesses": [3],
#     "incident_factors": [1, 2],

#     "immediate_actions": [
#         {
#             "title": "Notify IT team",
#             "description": "Inform IT to fix the system outage",
#             "employeeid": [5, 6]
#         }
#     ],

#     "improvement_recommendations": [
#         {
#             "action": "Upgrade software",
#             "action_description": "Upgrade system to latest version",
#             "responsible_employee_id": 5
#         }
#     ],

#     "followup_actions": [
#         {
#             "action_title": "Verify system stability",
#             "action_description": "Check system after upgrade",
#             "date_completed": "2025-08-20",
#             "responsible_employee": 5
#         }
#     ]
# }

class Document(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="uploads/")  
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"