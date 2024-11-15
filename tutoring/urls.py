from django.urls import path

from tutoring.views.payment_views import BankAccountListView, PaymentListCreateView, PaymentDetailView, \
    BankAccountDetailView, LessonPaymentListCreateView, LessonPaymentDetailView
from tutoring.views.user_views import TutorProfileListView, TutorProfileDetailView, StudentProfileListView, \
    StudentProfileDetailView, ParentProfileListView, ParentProfileDetailView, UserDetailView, \
    CurrentUserView
from tutoring.views.views import LessonListView, LessonDetailView, EducationLevelListView, SubjectListView

urlpatterns = [
    path('user/me/', CurrentUserView.as_view(), name='current-user'),
    path('tutors/', TutorProfileListView.as_view(), name='tutor-list'),
    path('tutors/<int:pk>/', TutorProfileDetailView.as_view(), name='tutor-detail'),
    path('students/', StudentProfileListView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentProfileDetailView.as_view(), name='student-detail'),
    path('parents/', ParentProfileListView.as_view(), name='parent-list'),
    path('parents/<int:pk>/', ParentProfileDetailView.as_view(), name='parent-detail'),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('bank-accounts/', BankAccountListView.as_view(), name='bankaccount-list'),
    path('bank-accounts/<int:pk>/', BankAccountDetailView.as_view(), name='bankaccount-detail'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('lesson-payments/', LessonPaymentListCreateView.as_view(), name='lessonpayment-list'),
    path('lesson-payments/<int:pk>/', LessonPaymentDetailView.as_view(), name='lessonpayment-detail'),
    path('education-levels/', EducationLevelListView.as_view(), name='education-level-list'),
    path('subjects/', SubjectListView.as_view(), name='subject-list'),
    path('api/user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]