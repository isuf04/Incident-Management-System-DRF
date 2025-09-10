from rest_framework import serializers
from .models import *
    # designation_name = serializers.CharField(source='designation_id.name', read_only=True)

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

        
class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ["first_name","last_name","email","password","role"]
        # fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Employee
        fields = ["id",'user_id', 'designation_id', 'job_title' , 'phone_no' , ]
        
        
class Stack_HolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stack_Holder
        fields = ['id', 'user_id']


        
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id" ,"first_name","last_name","email","password","role" ]  
    
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = Users(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


        
                
class IncidentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident_type
        fields = '__all__'

class IncidentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident_Status
        fields = '__all__'
        
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields ='__all__'
        
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class DepartmentPocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department_poc
        fields =["id",'department_id' , 'employee_id']
        
        
class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'
        
        


#class meta  >>>>>>>>> Its give instruction to Django how to work and its not store actual data 
#type of serializer

class ContributingFactor_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Contributing_Factor
        fields = '__all__'
        
class ImprovementRecommendationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Improvement_Recommendation
        fields = ['action', 'action_description',]
class FollowupActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Followup_Action
        fields = ['action_title', 'action_description',"date_completed"]
    
    
class ImmediateActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Immediate_Action
        fields = ['title', 'description',]


class IncidentTicketSerializer(serializers.ModelSerializer):
    #read write in the form of IDs only
    contributing_factor = serializers.PrimaryKeyRelatedField(
        queryset=Contributing_Factor.objects.all(), many=True, required=False
    )
    individualsinvolved = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), many=True, required=False
    )
    incidentwitnesses = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), many=True, required=False
    )
    incidentfactors = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), many=True, required=False)
    
    departments = serializers.PrimaryKeyRelatedField(
    queryset=Department.objects.all(), required=False
    )
    
    file = serializers.FileField(required=False, allow_null=True)  
    #Get return data in nested detail 
    improvementrecommendation = ImprovementRecommendationSerializer(many=True, read_only=True, source='improvement_recommendation_set')
    followupactions = FollowupActionSerializer(many=True, read_only=True, source='followup_action_set')
    immediateaction = ImmediateActionSerializer(many=True, read_only=True, source='immediate_action_set')

    class Meta:
        model = Incident_Ticket
        fields = [
            "id",
            "assinged_poc",
            "requestor_id",
            "report_type",
            "occurrence_date",
            "location",
            "departments",
            "risk_level",
            "facility",
            "description",
            "recurrence",
            "potential_severity",
            "improvementrecommendation",
            "followupactions",
            "immediateaction",
            "contributing_factor",
            "individualsinvolved",
            "incidentwitnesses",
            "incidentfactors",
            "file"
        ]
        # fields = '__all__'
        
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
        
        
