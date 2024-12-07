from django.urls import path

from tutoring.views.payment_views import BankAccountListView, BankAccountDetailView, LessonPaymentListCreateView, LessonPaymentDetailView
from tutoring.views.user_views import TutorProfileDetailView, StudentProfileListView, \
    StudentProfileDetailView, ParentProfileListView, ParentProfileDetailView, UserDetailView, \
    CurrentUserView, TutorListView, LessonCreateView, LessonAcceptView, UploadAvatarView, LessonDocumentUploadView, \
    LessonFeedbackView
from tutoring.views.views import LessonDetailView, EducationLevelListView, SubjectListView, StudentLessonListView, \
    TutorLessonListView, ParentLessonListView, UserWithMessagesListView, MessageListView, TutorSubjectPriceListView

urlpatterns = [
    path('user/me/', CurrentUserView.as_view(), name='current-user'),
    path('tutors/', TutorListView.as_view(), name='tutor-list'),
    path('tutors/<int:pk>/', TutorProfileDetailView.as_view(), name='tutor-detail'),
    path('students/', StudentProfileListView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentProfileDetailView.as_view(), name='student-detail'),
    path('parents/', ParentProfileListView.as_view(), name='parent-list'),
    path('parents/<int:pk>/', ParentProfileDetailView.as_view(), name='parent-detail'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('tutor/lessons/', TutorLessonListView.as_view(), name='tutor-lesson-list'),
    path('student/lessons/', StudentLessonListView.as_view(), name='student-lesson-list'),
    path('parent/lessons/', ParentLessonListView.as_view(), name='parent-lesson-list'),
    path('bank-accounts/', BankAccountListView.as_view(), name='bankaccount-list'),
    path('bank-accounts/<int:pk>/', BankAccountDetailView.as_view(), name='bankaccount-detail'),
    path('lesson-payments/', LessonPaymentListCreateView.as_view(), name='lessonpayment-list'),
    path('lesson-payments/<int:pk>/', LessonPaymentDetailView.as_view(), name='lessonpayment-detail'),
    path('education-levels/', EducationLevelListView.as_view(), name='education-level-list'),
    path('subjects/', SubjectListView.as_view(), name='subject-list'),
    path('tutor-subject-prices/', TutorSubjectPriceListView.as_view(), name='tutor-subject-price-list'),
    path('lessons-create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/', LessonDetailView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/accept', LessonAcceptView.as_view(), name='lesson-accept'),
    path('api/user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('messages/', MessageListView.as_view(), name='message-list'),
    path('users-with-messages/', UserWithMessagesListView.as_view(), name='users-with-messages'),
    path('upload-avatar/', UploadAvatarView.as_view(), name='upload-avatar'),
    path('lessons/<int:id>/documents/', LessonDocumentUploadView.as_view(), name='lesson-document-upload'),
    path('lessons/<int:id>/feedback/', LessonFeedbackView.as_view(), name='lesson-feedback'),
]
