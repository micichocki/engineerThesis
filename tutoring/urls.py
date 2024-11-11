from django.urls import path

from tutoring.views.payment_views import BankAccountListView, PaymentListCreateView, PaymentDetailView, \
    BankAccountDetailView, LessonPaymentListCreateView, LessonPaymentDetailView
from tutoring.views.user_views import TutorProfileListView, TutorProfileDetailView, StudentProfileListView, \
    StudentProfileDetailView, ParentProfileListView, ParentProfileDetailView
from tutoring.views.views import LessonListView, LessonDetailView

urlpatterns = [   path('api/tutors/', TutorProfileListView.as_view(), name='tutor-list'),
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