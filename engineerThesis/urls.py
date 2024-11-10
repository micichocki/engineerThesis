"""
URL configuration for engineerThesis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from tutoring.views import StudentProfileListView, StudentProfileDetailView, TutorProfileListView, \
    TutorProfileDetailView, LessonListView, \
    LessonDetailView, ParentProfileListView, ParentProfileDetailView, BankAccountListView, BankAccountDetailView, \
    PaymentListCreateView, PaymentDetailView, LessonPaymentListCreateView, LessonPaymentDetailView, RegisterView, \
    TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="App API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/tutors/', TutorProfileListView.as_view(), name='tutor-list'),
    path('api/tutors/<int:pk>/', TutorProfileDetailView.as_view(), name='tutor-detail'),
    path('api/students/', StudentProfileListView.as_view(), name='student-list'),
    path('api/students/<int:pk>/', StudentProfileDetailView.as_view(), name='student-detail'),
    path('api/parents/', ParentProfileListView.as_view(), name='parent-list'),
    path('api/parents/<int:pk>/', ParentProfileDetailView.as_view(), name='parent-detail'),
    path('api/lessons/', LessonListView.as_view(), name='lesson-list'),
    path('api/lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('api/bank-accounts/', BankAccountListView.as_view(), name='bankaccount-list'),
    path('api/bank-accounts/<int:pk>/', BankAccountDetailView.as_view(), name='bankaccount-detail'),
    path('api/payments/', PaymentListCreateView.as_view(), name='payment-list'),
    path('api/payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('api/lesson-payments/', LessonPaymentListCreateView.as_view(), name='lessonpayment-list'),
    path('api/lesson-payments/<int:pk>/', LessonPaymentDetailView.as_view(), name='lessonpayment-detail'),
]
