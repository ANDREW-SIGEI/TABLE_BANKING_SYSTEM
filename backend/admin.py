from django.contrib import admin
from .models import *

@admin.register(BankingGroup)
class BankingGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'county', 'constituency']
    search_fields = ['name', 'code']

@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ['member_name', 'id_number', 'phone', 'group', 'is_active']
    list_filter = ['group', 'is_active']
    search_fields = ['member_name', 'id_number', 'phone']

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['member', 'loan_type', 'loan_amount', 'status', 'application_date']
    list_filter = ['loan_type', 'status', 'application_date']
    search_fields = ['member__member_name']

@admin.register(SavingsContribution)
class SavingsContributionAdmin(admin.ModelAdmin):
    list_display = ['member', 'amount', 'contribution_type', 'contribution_date']
    list_filter = ['contribution_type', 'contribution_date']

@admin.register(FieldOfficer)
class FieldOfficerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'is_active']

@admin.register(OfficerTracking)
class OfficerTrackingAdmin(admin.ModelAdmin):
    list_display = ['officer', 'latitude', 'longitude', 'timestamp']
