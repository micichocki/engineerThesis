from django.urls import path

from tutoring.views.payment_views import BankAccountDetailView, LessonPaymentListCreateView
from tutoring.views.user_views import TutorProfileDetailView, StudentProfileListView, \
    StudentProfileDetailView, ParentProfileListView, ParentProfileDetailView, \
    CurrentUserView, TutorListView, LessonCreateView, LessonAcceptView, UploadAvatarView, LessonDocumentUploadView, \
    LessonFeedbackView
from tutoring.views.views import LessonDetailView, EducationLevelListView, SubjectListView, StudentLessonListView, \
    TutorLessonListView, ParentLessonListView, UserWithMessagesListView, MessageListView




urlpatterns = [
    path('user/me/', CurrentUserView.as_view(), name='current-user'),
    path('upload-avatar/', UploadAvatarView.as_view(), name='upload-avatar'),
    path('users-with-messages/', UserWithMessagesListView.as_view(), name='users-with-messages'),
    path('messages/', MessageListView.as_view(), name='message-list'),
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
    path('lessons-create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/accept', LessonAcceptView.as_view(), name='lesson-accept'),
    path('lesson-payments/', LessonPaymentListCreateView.as_view(), name='lessonpayment-list'),
    path('lessons/<int:id>/documents/', LessonDocumentUploadView.as_view(), name='lesson-document-upload'),
    path('lessons/<int:id>/feedback/', LessonFeedbackView.as_view(), name='lesson-feedback'),
    path('education-levels/', EducationLevelListView.as_view(), name='education-level-list'),
    path('subjects/', SubjectListView.as_view(), name='subject-list'),
    path('bank-accounts/<int:pk>/', BankAccountDetailView.as_view(), name='bankaccount-detail'),
]
