from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view,parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
import json









@api_view(['GET','POST','PUT' ,  'DELETE'])
def UsersView(request):
    if request.method == 'GET':
        users = Users.objects.all()
        
        paginator = PageNumberPagination()
        paginator.page_size = 5

        page = paginator.paginate_queryset(users, request)
        
        serializer = UsersSerializer(page, many=True)
        
        # Pagination response
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == "POST":
        post_data = request.data.copy()

        # fetching User  related fields 
        user_data = {
            "first_name": post_data.get("first_name"),
            "last_name": post_data.get("last_name"),
            "email": post_data.get("email"),
            "password": post_data.get("password"),
            "role": post_data.get("role"),
        }
        

        # fetching Employee aur StackHolder data 
        employee_data = post_data.get("employee")
        stackholder_data = post_data.get("stack_holder")

        # User serializer
        user_serializer = UsersSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            
            role_name = user.role.Name.lower()

            if role_name == 'employee' and employee_data:
                
                # Designation 
                try:
                    designation_obj = Designation.objects.get(id=employee_data.get("designation_id"))
                except Designation.DoesNotExist:
                    return Response({"error": "Invalid designation_id"}, status=status.HTTP_400_BAD_REQUEST)

                employee_obj = Employee(
                    user_id=user,
                    designation_id=designation_obj,
                    job_title=employee_data.get("job_title"),
                    phone_no=employee_data.get("phone_no"),
                )
                employee_obj.save()
                return Response({"message": "User and Employee created successfully."}, status=status.HTTP_201_CREATED)

            elif role_name == 'stack_holder' and stackholder_data is not None:
                stackholder_obj = Stack_Holder(user_id=user)
                stackholder_obj.save()
                return Response({"message": "User and StackHolder created successfully."}, status=status.HTTP_201_CREATED)

            else:
                return Response({"message": "User created but Role data missing or invalid."}, status=status.HTTP_201_CREATED)

        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
         
    elif request.method == 'PUT':
        try:
            user=Users.objects.get(id=request.data['id'])
            
            #update  fields
            user.first_name=request.data.get('first_name')
            user.last_name=request.data.get('last_name')
            user.email=request.data.get('email')
            user.save() 
            return Response({"message": "User updated"})
        except Users.DoesNotExist:
            return Response ({'error': "User Not Found"} , status=404)



    # elif request.method == 'DELETE':
    #     email= request.data.get('email')
        
    #     try:       
    #         user_del=Users.objects.get(email=email)
    #     except Users.DoesNotExist:
    #         return Response({"error": "User Not found"}, status=404)
    #     user_del.delete()
    #     return Response({"message": "User deleted"}) 
    
    
    elif request.method == 'DELETE':
        id= request.data.get('id')  
        try:       
            user_del=Users.objects.get(id=id)
        except Users.DoesNotExist:
            return Response({"error": "User Not found"}, status=404)
        user_del.delete()
        return Response({"message": "User Deleted"}) 



  
@api_view(['GET', 'PUT', 'DELETE'])
def EmployeeView(request):

    if request.method == 'GET':
        employee = Employee.objects.all()
        emps_serializer = EmployeeSerializer(employee, many=True)
        return Response(emps_serializer.data)
    

    
    

    
    elif request.method == 'PUT':
        try:
            emp_update=Employee.objects.get(id=request.data['id'])
            emp_update.job_title=request.data.get('job_title')
            emp_update.phone_no=request.data.get('phone_no')
            emp_update.save()
            return Response({"message": "Employee updated"})

        except Employee.DoesNotExist:
            return Response ({'error': "employee Not Found"} , status=404)


    elif request.method == 'DELETE':
        emp_id= request.data.get('id')       
        try:       
            emp_del=Employee.objects.get(id=emp_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee Not found"}, status=404)
        emp_del.delete()
        return Response({"message": f"Employee with this '{emp_id}' deleted"})
    

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def Incident_ticket(request):
    if request.method == 'GET':
        data = Incident_Ticket.objects.all()
        serializer = IncidentTicketSerializer(data, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST': 

        department_id = request.data.get('department')
        
        if not department_id:
            return Response({"error": "Department is required"}, status=400)

        try:
            department_poc = Department_poc.objects.get(department_id=department_id)
        except Department_poc.DoesNotExist:
            return Response({"error": "No POC found for this department"}, status=404)

        ticket_data = {
            "assinged_poc": department_poc.id,
            "requestor_id": request.data.get('requestor'),
            "report_type": request.data.get('report_type'),
            "occurrence_date": request.data.get('occurrence_date'),
            "location": request.data.get('location'),
            "departments": department_id,
            "risk_level": request.data.get('risk_level'),
            "facility": request.data.get('facility'),
            "description": request.data.get('description'),
            "recurrence": request.data.get('recurrence'),
            "potential_severity": request.data.get('potential_severity'),
            "file" :request.FILES.get("file")
        }

        serializer = IncidentTicketSerializer(data=ticket_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        ticket = serializer.save()

        # assing M2m fields
        ticket.contributing_factor.set(request.data.get('contributing_factors', []))
        ticket.individualsinvolved.set(request.data.get('individuals_involved', []))
        ticket.incidentwitnesses.set(request.data.get('incident_witnesses', []))
        ticket.incidentfactors.set(request.data.get('incident_factors', []))
        
        improvement_json = request.data.get('improvement_recommendations', '[]')
        try:
            improvement_list = json.loads(improvement_json)
        except json.JSONDecodeError:
            return Response({"error": "improvement_recommendations is not in valid formate"}, status=400)
        
        improvement_data = []
        for item in improvement_list:
            emp_id = item.get('responsible_employee_id')
            # if not emp_id:
            #     continue
            emp = Employee.objects.get(id=emp_id)
            obj = Improvement_Recommendation.objects.create(
                incidentid=ticket,
                action=item.get('action'),
                action_description=item.get('action_description'),
                responsible_employee_id=emp
            )
            improvement_data.append({
                "action": obj.action,
                "action_description": obj.action_description,
                "ResponsibleEmployee": f"{emp.user_id.first_name} {emp.user_id.last_name}"
            })
        
        
        immediate_actions_json = request.data.get('immediate_actions', '[]')
        try:
            immediate_actions_list = json.loads(immediate_actions_json)
        except json.JSONDecodeError:
            return Response({"error": "immediate_actions is not in valid formate"}, status=400)
        
        immediate_actions_data = []
        for item in immediate_actions_list:
            emp_id = item.get('employeeid')                                                                                                                               
            emp = Employee.objects.get(id=emp_id)
            obj = Immediate_Action.objects.create(
                incidentid=ticket,
                title=item.get('title'),
                description=item.get('description'),
                employeeid=emp
            )
            immediate_actions_data.append({
                "title": obj.title,
                "description": obj.description,
                "Employees": [f"{emp.user_id.first_name} {emp.user_id.last_name}"]
            })

        

        followup_actions_json = request.data.get('followup_actions', '[]') 
        try:
            followup_actions_list = json.loads(followup_actions_json)
        except json.JSONDecodeError:
            return Response({"error": "followup_actions is not in valid formate"}, status=400)

        followup_data = []
        for item in followup_actions_list:
        # for item in request.data.get('followup_actions', []):
            emp_id = item.get('responsible_employee')
            emp = Employee.objects.get(id=emp_id)
            obj = Followup_Action.objects.create(
                incidentid=ticket,
                action_title=item.get('action_title'),
                action_description=item.get('action_description'),
                date_completed=item.get('date_completed'),
                responsible_employee=emp
            )
            followup_data.append({
                "action_title": obj.action_title,
                "action_description": obj.action_description,
                "date_completed": obj.date_completed,
                "ResponsibleEmployee": f"{emp.user_id.first_name} {emp.user_id.last_name}"
            })
        
            
        contributing_factors = []
        for cont in ticket.contributing_factor.all():
            contributing_factors.append(cont.name)
        
        individuals_involved = []
        for emp in ticket.individualsinvolved.all():
            individuals_involved.append(emp.id)

        witnesses = []
        for emp in ticket.incidentwitnesses.all():
            witnesses.append(emp.id)

        incident_factors = []
        for emp in ticket.incidentfactors.all():
            incident_factors.append(emp.id)
        
        poc=ticket.assinged_poc
        employeee=poc.employee_id
        usersss=employeee.user_id 
       
        try:
            file_url = ticket.file.url
        except Exception:
            file_url = None



          
        final_data = {
            "Ticket_Id": ticket.id,
            "Department": ticket.departments.name,
            "Assign_poc": f"{usersss.first_name} {usersss.last_name}",
            "Contributingfactor": contributing_factors,
            "Individualsinvolved": individuals_involved,
            "Witnesses": witnesses,
            "Incident_factors": incident_factors,
            "ImmediateActions": immediate_actions_data,
            "Improvementrecommendation": improvement_data,
            "Followupactions": followup_data,
            "Risk_level": ticket.risk_level,
            "Location": ticket.location,
            "Facility": ticket.facility,
            "Description": ticket.description,
            "Recurrence": ticket.recurrence,
            "Potential_severity": ticket.potential_severity,
            "File":  file_url                                                                                                                                   #ticket.file.url if ticket.file else None

        }

        return Response(final_data, status=201)


@api_view(['GET', 'POST'])
def incident_type(request):
    if request.method == 'GET':
        data = Incident_type.objects.all()
        serializer = IncidentTypeSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = IncidentTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
 
@api_view(['GET', 'POST'])
def incident_Status(request):
    if request.method == 'GET':
        data = Incident_Status.objects.all()
        serializer = IncidentStatusSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = IncidentStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'POST'])
def Statusview(request):
    if request.method == 'GET':
        data = Status.objects.all()
        serializer = StatusSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
def Designation_View(request):
    if request.method == 'GET':
        data = Designation.objects.all()
        serializer = DesignationSerializer(data, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DesignationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['GET', 'POST'])
def Department_View(request):
    if request.method == 'GET':
        data = Department.objects.all()
        serializer = DepartmentSerializer(data, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['GET', 'PUT'])
def Stackholder_view(request):
    if request.method == 'GET':
        data = Stack_Holder.objects.all()
        serializer = Stack_HolderSerializer(data, many=True)
        return Response(serializer.data)



@api_view(['GET', 'POST'])
def DepartmentPoc_View(request):
    if request.method == 'GET':
        data = Department_poc.objects.all()
        serializer = DepartmentPocSerializer(data, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DepartmentPocSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400) 
     
@api_view(['GET', 'POST'])
def Role_View(request):
    if request.method == 'GET':
        data = Role.objects.all()
        role_serializer = RoleSerializer(data, many=True)
        return Response(role_serializer.data)
    
    # elif request.method == 'POST':
    #     ro_serializer = RoleSerializer(data=request.data)
    #     if ro_serializer.is_valid():
    #         ro_serializer.save()
    #         return Response(ro_serializer.data, status=201)
    #     return Response(ro_serializer.errors, status=400)   


@api_view(['GET', 'POST'])
def Contributing_factor_View(request):
    if request.method == 'GET':
        data= Contributing_Factor.objects.all()
        con_fact_serializer= ContributingFactor_Serializer(data, many=True)
        return Response (con_fact_serializer.data)
    
    # elif request.method == 'POST':
    #     co_fact= ContributingFactor_Serializer(data=request.data)
    #     if co_fact.is_valid():
    #         co_fact.save()
    #         return Response(co_fact.data , status=201)
    #     return Response(co_fact.errors , status=400)




@api_view(["GET", "POST"])
def improvement_recommendation_api(request):
    if request.method == "GET":
        recs = Improvement_Recommendation.objects.all()
        serializer = ImprovementRecommendationSerializer(recs, many=True)
        return Response(serializer.data)

    # # elif request.method == "POST":
    #     serializer = ImprovementRecommendationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def followup_action_api(request):
    if request.method == "GET":
        actions = Followup_Action.objects.all()
        serializer = FollowupActionSerializer(actions, many=True)
        return Response(serializer.data)

    # elif request.method == "POST":
    #     serializer = FollowupActionSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def immediate_action_api(request):
    if request.method == "GET":
        actions = Immediate_Action.objects.all()
        serializer = ImmediateActionSerializer(actions, many=True)
        return Response(serializer.data)

    # elif request.method == "POST":
    #     serializer = ImmediateActionSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.permissions import AllowAny
class LoginView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        print(email,password)
        
        user = authenticate(email = email, password = password)

        if user is not None:
            refresh = RefreshToken.for_user(user)         

            return Response({
                'access token': str(refresh.access_token),
                'refresh token': str(refresh)
            })
        else:
            return Response({'error': 'Invalid email or password'}, status = status.HTTP_401_UNAUTHORIZED)      

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)                           
            token.blacklist()
            return Response({ "succesfully logout"} , status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)}) 
        
   
@api_view(['POST' , 'GET'])
@parser_classes([MultiPartParser, FormParser])
def document_upload_view(request):
    if request.method == 'GET' :
        data = Document.objects.all()
        serializer = DocumentSerializer(data, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # print("DATA:", request.data)
        # print("FILES:", request.FILES)
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        
        
        
        
        
        
        
        









hello=[1,2,3,4,5,6]

    # if request.method == "GET":
        
    #     empdata = Employee.objects.all()
    #     employeedata = EmployeeSerializer(empdata, many=True)
    
    #     dataa = []
    #     for d in employeedata.data:
    #         response = {
    #             "id": d["id"],
    #             "user_id": d["user_id"],
    #             "user_email": d["user_email"], 
    #             "designation_id": d["designation_id"],
    #             "job_title": d["job_title"],
    #             "phone_no": d["phone_no"],
    #         }
    #         dataa.append(response)
        
    #     return Response(dataa)
    
    

    
