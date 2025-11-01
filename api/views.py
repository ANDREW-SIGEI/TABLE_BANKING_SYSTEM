from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from backend.models import *
from .serializers import *

class BankingGroupViewSet(viewsets.ModelViewSet):
    queryset = BankingGroup.objects.all()
    serializer_class = BankingGroupSerializer

class GroupMemberViewSet(viewsets.ModelViewSet):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer

class LoanApplicationViewSet(viewsets.ModelViewSet):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer

class SavingsContributionViewSet(viewsets.ModelViewSet):
    queryset = SavingsContribution.objects.all()
    serializer_class = SavingsContributionSerializer

class LoginView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        
        # For demo purposes, we'll use username instead of phone
        user = authenticate(username=phone, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'access_token': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })
        return Response({
            'success': False,
            'message': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

class DashboardStatsView(APIView):
    def get(self, request):
        total_groups = BankingGroup.objects.count()
        total_members = GroupMember.objects.count()
        active_loans = LoanApplication.objects.filter(status='APPROVED').count()
        
        # Calculate total savings
        savings_contributions = SavingsContribution.objects.all()
        total_savings = sum([s.amount for s in savings_contributions])
        
        return Response({
            'total_groups': total_groups,
            'total_members': total_members,
            'active_loans': active_loans,
            'total_savings': float(total_savings),
        })

class TrackOfficerView(APIView):
    def post(self, request):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        
        # Here you would typically get the officer from the authenticated user
        # For now, we'll just return success
        return Response({
            'success': True,
            'message': 'Location tracked successfully'
        })
