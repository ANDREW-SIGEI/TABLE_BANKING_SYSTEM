from rest_framework import serializers
from backend.models import *

class BankingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankingGroup
        fields = '__all__'

class GroupMemberSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    
    class Meta:
        model = GroupMember
        fields = '__all__'

class LoanApplicationSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.member_name', read_only=True)
    group_name = serializers.CharField(source='member.group.name', read_only=True)
    
    class Meta:
        model = LoanApplication
        fields = '__all__'

class SavingsContributionSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.member_name', read_only=True)
    
    class Meta:
        model = SavingsContribution
        fields = '__all__'

class FieldOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfficer
        fields = '__all__'

class OfficerTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficerTracking
        fields = '__all__'
