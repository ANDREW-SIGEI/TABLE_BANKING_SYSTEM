from django.db import models
from django.contrib.auth.models import User

class BankingGroup(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    county = models.CharField(max_length=100)
    constituency = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    meeting_day = models.CharField(max_length=20)
    meeting_venue = models.CharField(max_length=255)
    registration_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class GroupMember(models.Model):
    group = models.ForeignKey(BankingGroup, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    registration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.member_name

class LoanApplication(models.Model):
    LOAN_TYPES = [
        ('SHORT_TERM', 'Short Term (< 3 months)'),
        ('LONG_TERM', 'Long Term'),
        ('PROJECT', 'Project Loan'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('DISBURSED', 'Disbursed'),
    ]
    
    member = models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    duration_months = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    purpose = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    application_date = models.DateField(auto_now_add=True)
    approved_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.member.member_name} - {self.loan_amount}"

class SavingsContribution(models.Model):
    CONTRIBUTION_TYPES = [
        ('REGULAR', 'Regular Savings'),
        ('WELFARE', 'Welfare'),
        ('PROJECT', 'Project'),
        ('FINE', 'Fine'),
    ]
    
    member = models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    contribution_type = models.CharField(max_length=20, choices=CONTRIBUTION_TYPES)
    contribution_date = models.DateField()
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.member.member_name} - {self.amount}"

class FieldOfficer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    assigned_groups = models.ManyToManyField(BankingGroup)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.get_full_name()

class OfficerTracking(models.Model):
    officer = models.ForeignKey(FieldOfficer, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.officer} - {self.timestamp}"
