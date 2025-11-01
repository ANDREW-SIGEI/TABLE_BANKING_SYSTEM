from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('groups', views.BankingGroupViewSet)
router.register('members', views.GroupMemberViewSet)
router.register('loans', views.LoanApplicationViewSet)
router.register('savings', views.SavingsContributionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('dashboard/stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
    path('officer/track/', views.TrackOfficerView.as_view(), name='track-officer'),
]
