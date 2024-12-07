import pytest
from django.contrib.auth import get_user_model
from tutoring.models import Role, TutorProfile, StudentProfile, ParentProfile, WorkingExperience, EducationLevel, AvailableHour, Subject, Lesson, LessonDocument, BankAccount, LessonPayment, TutorSubjectPrice, Message, GoogleCredentials

User = get_user_model()

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(username='testuser', password='password123')
    assert user.username == 'testuser'

@pytest.mark.django_db
def test_role_creation():
    role = Role.objects.create(name='NewRole')
    assert role.name == 'NewRole'

@pytest.mark.django_db
def test_tutor_profile_creation():
    user = User.objects.create_user(username='tutoruser', password='password123')
    tutor_profile = TutorProfile.objects.create(user=user)
    assert tutor_profile.user.username == 'tutoruser'

@pytest.mark.django_db
def test_student_profile_creation():
    user = User.objects.create_user(username='studentuser', password='password123')
    student_profile = StudentProfile.objects.create(user=user)
    assert student_profile.user.username == 'studentuser'

@pytest.mark.django_db
def test_parent_profile_creation():
    user = User.objects.create_user(username='parentuser', password='password123')
    parent_profile = ParentProfile.objects.create(user=user)
    assert parent_profile.user.username == 'parentuser'

@pytest.mark.django_db
def test_working_experience_creation():
    experience = WorkingExperience.objects.create(position='Teacher', start_date='2020-01-01')
    assert experience.position == 'Teacher'

@pytest.mark.django_db
def test_education_level_creation():
    education_level = EducationLevel.objects.create(level='primary')
    assert education_level.level == 'primary'

@pytest.mark.django_db
def test_available_hour_creation():
    available_hour = AvailableHour.objects.create(day_of_week='Monday', start_time='09:00', end_time='10:00')
    assert available_hour.day_of_week == 'Monday'

@pytest.mark.django_db
def test_subject_creation():
    subject = Subject.objects.create(name='Math')
    assert subject.name == 'Math'

@pytest.mark.django_db
def test_lesson_creation():
    tutor_user = User.objects.create_user(username='tutoruser', password='password123')
    student_user = User.objects.create_user(username='studentuser', password='password123')
    tutor_profile = TutorProfile.objects.create(user=tutor_user)
    student_profile = StudentProfile.objects.create(user=student_user)
    subject = Subject.objects.create(name='Math')
    lesson = Lesson.objects.create(tutor=tutor_profile, student=student_profile, subject=subject, start_time='2023-01-01T10:00:00Z', end_time='2023-01-01T11:00:00Z', price_per_hour=50.00)
    assert lesson.tutor.user.username == 'tutoruser'
    assert lesson.student.user.username == 'studentuser'
    assert lesson.subject.name == 'Math'

@pytest.mark.django_db
def test_lesson_document_creation():
    tutor_user = User.objects.create_user(username='tutoruser', password='password123')
    student_user = User.objects.create_user(username='studentuser', password='password123')
    tutor_profile = TutorProfile.objects.create(user=tutor_user)
    student_profile = StudentProfile.objects.create(user=student_user)
    subject = Subject.objects.create(name='Math')
    lesson = Lesson.objects.create(tutor=tutor_profile, student=student_profile, subject=subject, start_time='2023-01-01T10:00:00Z', end_time='2023-01-01T11:00:00Z', price_per_hour=50.00)
    lesson_document = LessonDocument.objects.create(lesson=lesson, document='path/to/document.pdf')
    assert lesson_document.lesson == lesson

@pytest.mark.django_db
def test_bank_account_creation():
    user = User.objects.create_user(username='bankuser', password='password123')
    bank_account = BankAccount.objects.create(user=user, account_number='1234567890', bank_name='BankName')
    assert bank_account.user.username == 'bankuser'

@pytest.mark.django_db
def test_lesson_payment_creation():
    tutor_user = User.objects.create_user(username='tutoruser', password='password123')
    student_user = User.objects.create_user(username='studentuser', password='password123')
    tutor_profile = TutorProfile.objects.create(user=tutor_user)
    student_profile = StudentProfile.objects.create(user=student_user)
    subject = Subject.objects.create(name='Math')
    lesson = Lesson.objects.create(tutor=tutor_profile, student=student_profile, subject=subject, start_time='2023-01-01T10:00:00Z', end_time='2023-01-01T11:00:00Z', price_per_hour=50.00)
    lesson_payment = LessonPayment.objects.create(lesson=lesson, payment_status='Paid', amount=50.00)
    assert lesson_payment.lesson == lesson

@pytest.mark.django_db
def test_tutor_subject_price_creation():
    tutor_user = User.objects.create_user(username='tutoruser', password='password123')
    tutor_profile = TutorProfile.objects.create(user=tutor_user)
    subject = Subject.objects.create(name='Math')
    tutor_subject_price = TutorSubjectPrice.objects.create(tutor=tutor_profile, subject=subject, price_min=30.00, price_max=50.00)
    assert tutor_subject_price.tutor == tutor_profile
    assert tutor_subject_price.subject == subject

@pytest.mark.django_db
def test_message_creation():
    sender = User.objects.create_user(username='senderuser', password='password123')
    recipient = User.objects.create_user(username='recipientuser', password='password123')
    message = Message.objects.create(sender=sender, recipient=recipient, content='Hello!')
    assert message.sender.username == 'senderuser'
    assert message.recipient.username == 'recipientuser'

@pytest.mark.django_db
def test_google_credentials_creation():
    user = User.objects.create_user(username='googleuser', password='password123')
    google_credentials = GoogleCredentials.objects.create(user=user, token='token', refresh_token='refresh_token', token_uri='token_uri', client_id='client_id', client_secret='client_secret', scopes='scopes')
    assert google_credentials.user.username == 'googleuser'