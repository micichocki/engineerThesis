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

from tutoring.views import StudentListView, StudentDetailView, TutorListView, TutorDetailView, LessonListView, \
    LessonDetailView, ParentListView, ParentDetailView, BankAccountListView, BankAccountDetailView, \
    PaymentListCreateView, PaymentDetailView, LessonPaymentListCreateView, LessonPaymentDetailView

urlpatterns = [
    path('tutors/', TutorListView.as_view(), name='tutor-list'),
    path('tutors/<int:pk>/', TutorDetailView.as_view(), name='tutor-detail'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('parents/', ParentListView.as_view(), name='parent-list'),
    path('parents/<int:pk>/', ParentDetailView.as_view(), name='parent-detail'),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('bank-accounts/', BankAccountListView.as_view(), name='bankaccount-list'),
    path('bank-accounts/<int:pk>/', BankAccountDetailView.as_view(), name='bankaccount-detail'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('lesson-payments/', LessonPaymentListCreateView.as_view(), name='lessonpayment-list'),
    path('lesson-payments/<int:pk>/', LessonPaymentDetailView.as_view(), name='lessonpayment-detail'),
]
