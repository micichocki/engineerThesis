import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
from rest_framework import status

from tutoring.models import User, Message, TutorProfile, Subject, StudentProfile, EducationLevel, \
    ParentProfile, Lesson, LessonPayment, BankAccount
from tutoring.views.user_views import CurrentUserView, UploadAvatarView
from tutoring.views.views import UserWithMessagesListView, MessageListView


@pytest.mark.django_db
def test_current_user_view_without_tokens():
    user = User.objects.create_user(username='testuser', password='password123')

    factory = APIRequestFactory()

    request = factory.get('/user/me/')

    force_authenticate(request, user=user)

    view = CurrentUserView.as_view()
    response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == 'testuser'

@pytest.mark.django_db
def test_upload_avatar_view():
    user = User.objects.create_user(username='testuser', password='password123')

    factory = APIRequestFactory()

    image_file = SimpleUploadedFile("test_avatar.jpg", b"file_content", content_type="image/jpeg")

    request = factory.post('/upload-avatar/', {'avatar': image_file}, format='multipart')

    force_authenticate(request, user=user)

    view = UploadAvatarView.as_view()
    response = view(request)

    assert response.status_code == status.HTTP_200_OK

    assert response.data['success'] == 'Avatar uploaded successfully'

@pytest.mark.django_db
def test_user_with_messages_list_view():
    user1 = User.objects.create_user(username='user1', password='password123')
    user2 = User.objects.create_user(username='user2', password='password123')
    user3 = User.objects.create_user(username='user3', password='password123')

    Message.objects.create(sender=user1, recipient=user2, content='Hello user2')
    Message.objects.create(sender=user2, recipient=user1, content='Hello user1')
    Message.objects.create(sender=user1, recipient=user3, content='Hello user3')

    factory = APIRequestFactory()

    request = factory.get('/users-with-messages/')

    force_authenticate(request, user=user1)

    view = UserWithMessagesListView.as_view()
    response = view(request)

    assert response.status_code == status.HTTP_200_OK

    user_ids = {user2.id, user3.id}
    response_user_ids = {user['id'] for user in response.data}
    assert response_user_ids == user_ids


@pytest.mark.django_db
def test_message_list_view():
    user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password123')
    user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password123')

    Message.objects.create(sender=user1, recipient=user2, content='Hello user2')
    Message.objects.create(sender=user2, recipient=user1, content='Hello user1')

    factory = APIRequestFactory()

    request = factory.get('/messages/', {'recipient': 'user2@example.com'})

    force_authenticate(request, user=user1)

    view = MessageListView.as_view()
    response = view(request)

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 2
    assert response.data[0]['content'] == 'Hello user2'
    assert response.data[1]['content'] == 'Hello user1'


# @pytest.mark.django_db
# def test_tutor_list_view_with_filters():
#     user1 = User.objects.create_user(username="tutor1", password="password123", city="CityA")
#     user2 = User.objects.create_user(username="tutor2", password="password123", city="CityB")
#
#     subject_math = Subject.objects.create(name="Math")
#     subject_science = Subject.objects.create(name="Science")
#
#     profile1 = TutorProfile.objects.create(user=user1, is_remote=True)
#     profile2 = TutorProfile.objects.create(user=user2, is_remote=False)
#
#     TutorSubjectPrice.objects.create(tutor=profile1, subject=subject_math, price_min=50, price_max=100)
#     TutorSubjectPrice.objects.create(tutor=profile2, subject=subject_science, price_min=30, price_max=80)
#
#     factory = APIRequestFactory()
#     view = TutorListView.as_view()
#
#     request = factory.get(
#         "/tutors/",
#         {
#             "city": "CityA",
#             "subject": "Math",
#             "min_price": 40,
#             "max_price": 90,
#             "remote_only": "true",
#         },
#     )
#     request.user = user1
#
#     response = view(request)
#     print(response.data)
#     assert response.status_code == 200
#     assert len(response.data) == 1
#     assert response.data[0]["username"] == "tutor1"
#     assert response.data[0]["city"] == "CityA"
#     assert "Math" in response.data[0]["subjects"]
#     assert float(response.data[0]["subject_prices"][0]["price_min"]) == 50
#     assert float(response.data[0]["subject_prices"][0]["price_max"]) == 100

class TutorProfileDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.tutor_profile = TutorProfile.objects.create(user=self.user, bio='Test bio')
        self.subject = Subject.objects.create(name='Math')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('tutor-detail', kwargs={'pk': self.tutor_profile.pk})

    def test_update_tutor_profile(self):
        data = {
            'bio': 'Updated bio',
            'working_experience': [
                {
                    'position': 'Teacher',
                    'start_date': '2020-01-01',
                    'end_date': '2021-01-01',
                    'description': 'Taught math'
                }
            ],
            'subject_prices': [
                {
                    'name': 'Math',
                    'min_price': 20,
                    'max_price': 40
                }
            ],
            'available_hours': 'Monday:09:00-12:00;Tuesday:13:00-15:00',
            'city': 'New City',
            'is_remote': True
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.tutor_profile.refresh_from_db()
        self.assertEqual(self.tutor_profile.bio, 'Updated bio')
        self.assertEqual(self.tutor_profile.user.city, 'New city')
        self.assertTrue(self.tutor_profile.is_remote)
        self.assertEqual(self.tutor_profile.working_experience.count(), 1)
        self.assertEqual(self.tutor_profile.subjects.count(), 1)
        self.assertEqual(self.tutor_profile.available_hours.count(), 2)

    def test_invalid_subject(self):
        data = {
            'subject_prices': [
                {
                    'name': 'InvalidSubject',
                    'min_price': 20,
                    'max_price': 40
                }
            ]
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid subject', response.data['error'])

    def test_invalid_time_format(self):
        data = {
            'available_hours': 'Monday:09:00-12:00;Tuesday:invalid-time'
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid time format', response.data['error'])

    def test_start_time_greater_than_end_time(self):
        data = {
            'available_hours': 'Monday:12:00-09:00'
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Start time cannot be greater than or equal to end time', response.data['error'])


class StudentProfileListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('student-list')

    def test_list_student_profiles(self):
        StudentProfile.objects.create(user=self.user, bio='Test bio')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['bio'], 'Test bio')

class StudentProfileDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.student_profile = StudentProfile.objects.create(user=self.user, bio='Test bio')
        self.education_level = EducationLevel.objects.create(level='High School')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('student-detail', kwargs={'pk': self.student_profile.pk})

    def test_update_student_profile(self):
        data = {
            'bio': 'Updated bio',
            'tasks_description': 'Updated tasks description',
            'goal': 'Updated goal',
            'education_level': self.education_level.level,
            'available_hours': 'Monday:09:00-12:00;Tuesday:13:00-15:00'
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student_profile.refresh_from_db()
        self.assertEqual(self.student_profile.bio, 'Updated bio')
        self.assertEqual(self.student_profile.tasks_description, 'Updated tasks description')
        self.assertEqual(self.student_profile.goal, 'Updated goal')
        self.assertEqual(self.student_profile.education_level, self.education_level)
        self.assertEqual(self.student_profile.available_hours.count(), 2)

    def test_invalid_time_format(self):
        data = {
            'available_hours': 'Monday:09:00-12:00;Tuesday:invalid-time'
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid time format', response.data['error'])

    def test_start_time_greater_than_end_time(self):
        data = {
            'available_hours': 'Monday:12:00-09:00'
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Start time cannot be greater than or equal to end time', response.data['error'])


class ParentProfileListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('parent-list')

    def test_list_parent_profiles(self):
        ParentProfile.objects.create(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.user.parentprofile.id)

class ParentProfileDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.parent_profile = ParentProfile.objects.create(user=self.user)
        self.student_profile = StudentProfile.objects.create(user=self.user, bio='Test bio')
        self.url = reverse('parent-detail', kwargs={'pk': self.parent_profile.pk})

    def test_update_parent_profile(self):
        data = {
            'children': [self.student_profile.user.email]
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.parent_profile.refresh_from_db()
        self.assertEqual(list(self.parent_profile.children.all()), [self.student_profile])

class LessonDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.tutor_profile = TutorProfile.objects.create(user=self.user)
        self.student_profile = StudentProfile.objects.create(user=self.user)
        self.subject = Subject.objects.create(name='Math')
        self.lesson = Lesson.objects.create(
            tutor=self.tutor_profile,
            student=self.student_profile,
            subject=self.subject,
            start_time='2023-10-10T10:00:00Z',
            end_time='2023-10-10T11:00:00Z',
            price_per_hour=30.0,
            is_remote=True,
            description='Test lesson'
        )
        self.url = reverse('lesson-detail', kwargs={'pk': self.lesson.id})

    def test_retrieve_lesson(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Test lesson')

    def test_delete_lesson(self):
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

class TutorLessonListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.tutor_profile = TutorProfile.objects.create(user=self.user)
        self.student_profile = StudentProfile.objects.create(user=self.user)
        self.subject = Subject.objects.create(name='Math')
        self.lesson = Lesson.objects.create(
            tutor=self.tutor_profile,
            student=self.student_profile,
            subject=self.subject,
            start_time='2023-10-10T10:00:00Z',
            end_time='2023-10-10T11:00:00Z',
            description='Test Lesson',
            price_per_hour=50.0
        )
        self.url = reverse('tutor-lesson-list')

    def test_list_tutor_lessons(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.lesson.id)


class LessonListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.tutor_profile = TutorProfile.objects.create(user=self.user)
        self.student_profile = StudentProfile.objects.create(user=self.user)
        self.parent_profile = ParentProfile.objects.create(user=self.user)
        self.subject = Subject.objects.create(name='Math')
        self.lesson = Lesson.objects.create(
            tutor=self.tutor_profile,
            student=self.student_profile,
            subject=self.subject,
            start_time='2023-10-10T10:00:00Z',
            end_time='2023-10-10T11:00:00Z',
            description='Test Lesson',
            price_per_hour=50.0
        )
        self.parent_profile.children.add(self.student_profile)
        self.tutor_url = reverse('tutor-lesson-list')
        self.student_url = reverse('student-lesson-list')
        self.parent_url = reverse('parent-lesson-list')

    def test_list_tutor_lessons(self):
        response = self.client.get(self.tutor_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.lesson.id)

    def test_list_student_lessons(self):
        response = self.client.get(self.student_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.lesson.id)

    def test_list_parent_lessons(self):
        response = self.client.get(self.parent_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertEqual(response.data[0]['id'], self.lesson.id)


class LessonCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.tutor_profile = TutorProfile.objects.create(user=self.user)
        self.student_profile = StudentProfile.objects.create(user=self.user)
        self.subject = Subject.objects.create(name='Math')
        self.url = reverse('lesson-create')

    def test_create_lesson(self):
        data = {
            'tutor': self.tutor_profile.id,
            'student': self.student_profile.id,
            'subject': self.subject.id,
            'date': '2023-10-10',
            'start_time': '10:00',
            'end_time': '11:00',
            'price_per_hour': 50.0
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(tutor=self.tutor_profile, student=self.student_profile,
                                              subject=self.subject).exists())

    def test_create_lesson_with_existing_lesson(self):
        Lesson.objects.create(
            tutor=self.tutor_profile,
            student=self.student_profile,
            subject=self.subject,
            start_time='2023-10-10T10:00:00Z',
            end_time='2023-10-10T11:00:00Z',
            price_per_hour=50.0
        )
        data = {
            'tutor': self.tutor_profile.id,
            'student': self.student_profile.id,
            'subject': self.subject.id,
            'date': '2023-10-10',
            'start_time': '10:00',
            'end_time': '11:00'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'A lesson with the same tutor, student, and subject already exists for this date.')


class LessonAcceptViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.tutor_profile = TutorProfile.objects.create(user=self.user)
        self.student_profile = StudentProfile.objects.create(user=self.user)
        self.subject = Subject.objects.create(name='Math')
        self.lesson = Lesson.objects.create(
            tutor=self.tutor_profile,
            student=self.student_profile,
            subject=self.subject,
            start_time='2023-10-10T10:00:00Z',
            end_time='2023-10-10T11:00:00Z',
            price_per_hour=50.0
        )
        self.url = reverse('lesson-accept', kwargs={'pk': self.lesson.pk})

    def test_accept_lesson(self):
        data = {
            'is_accepted': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertTrue(self.lesson.is_accepted)

    def test_accept_nonexistent_lesson(self):
        url = reverse('lesson-accept', kwargs={'pk': 999})
        data = {
            'is_accepted': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class LessonPaymentListCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.tutor_profile = TutorProfile.objects.create(user=self.user)
        self.student_profile = StudentProfile.objects.create(user=self.user)
        self.subject = Subject.objects.create(name='Math')
        self.lesson = Lesson.objects.create(
            tutor=self.tutor_profile,
            student=self.student_profile,
            subject=self.subject,
            start_time='2023-10-10T10:00:00Z',
            end_time='2023-10-10T11:00:00Z',
            price_per_hour=50.0
        )
        self.url = reverse('lessonpayment-list')

    def test_list_lesson_payments(self):
        LessonPayment.objects.create(
            lesson=self.lesson,
            payment_status='Paid',
            amount=50.0
        )
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['payment_status'], 'Paid')

    def test_create_lesson_payment(self):
        data = {
            'lesson': self.lesson.id,
            'payment_status': 'Paid',
            'amount': 50.0
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(LessonPayment.objects.filter(lesson=self.lesson, payment_status='Paid').exists())

class LessonDocumentUploadViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.tutor_profile = TutorProfile.objects.create(user=self.user)
        self.student_profile = StudentProfile.objects.create(user=self.user)
        self.subject = Subject.objects.create(name='Math')
        self.lesson = Lesson.objects.create(
            tutor=self.tutor_profile,
            student=self.student_profile,
            subject=self.subject,
            start_time='2023-10-10T10:00:00Z',
            end_time='2023-10-10T11:00:00Z',
            price_per_hour=50.0
        )
        self.url = reverse('lesson-document-upload', kwargs={'id': self.lesson.id})

    def test_upload_document(self):
        document = SimpleUploadedFile("document.pdf", b"file_content", content_type="application/pdf")
        data = {'document': document}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.lesson.documents.exists())

    def test_upload_large_document(self):
        large_content = b"a" * (1 * 1024 * 1024 * 1024 + 1)
        document = SimpleUploadedFile("document.pdf", large_content, content_type="application/pdf")
        data = {'document': document}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "File size exceeds 1 GB limit")

    def test_upload_non_pdf_document(self):
        document = SimpleUploadedFile("document.txt", b"file_content", content_type="text/plain")
        data = {'document': document}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Only PDF files are allowed")

class LessonFeedbackViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.tutor_profile = TutorProfile.objects.create(user=self.user)
        self.student_profile = StudentProfile.objects.create(user=self.user)
        self.subject = Subject.objects.create(name='Math')
        self.lesson = Lesson.objects.create(
            tutor=self.tutor_profile,
            student=self.student_profile,
            subject=self.subject,
            start_time='2023-10-10T10:00:00Z',
            end_time='2023-10-10T11:00:00Z',
            price_per_hour=50.0
        )
        self.url = reverse('lesson-feedback', kwargs={'id': self.lesson.id})

    def test_post_feedback(self):
        data = {
            'rating': 5,
            'feedback': 'Great lesson!'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.rating, 5)
        self.assertEqual(self.lesson.feedback, 'Great lesson!')

    def test_post_feedback_lesson_not_found(self):
        url = reverse('lesson-feedback', kwargs={'id': 999})
        data = {
            'rating': 5,
            'feedback': 'Great lesson!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Lesson not found')

    def test_post_feedback_already_exists(self):
        self.lesson.rating = 5
        self.lesson.feedback = 'Great lesson!'
        self.lesson.save()
        data = {
            'rating': 4,
            'feedback': 'Good lesson!'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'This lesson already has a rating or comment')

class EducationLevelListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('education-level-list')

    def test_list_education_levels(self):
        EducationLevel.objects.create(level='High School')
        EducationLevel.objects.create(level='Bachelor')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0]['level'], 'primary')
        self.assertEqual(response.data[1]['level'], 'secondary')


class SubjectListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('subject-list')

    def test_list_subjects(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)
        self.assertEqual(response.data[0]['name'], 'Mathematics')
        self.assertEqual(response.data[1]['name'], 'English')

    def test_create_subject(self):
        data = {'name': 'History'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subject.objects.filter(name='History').exists())


class BankAccountDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.bank_account = BankAccount.objects.create(
            user=self.user,
            account_number='1234567890',
            bank_name='Test Bank'
        )
        self.url = reverse('bankaccount-detail', kwargs={'pk': self.bank_account.id})

    def test_retrieve_bank_account(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['account_number'], '1234567890')
        self.assertEqual(response.data['bank_name'], 'Test Bank')

    def test_update_bank_account(self):
        data = {'account_number': '0987654321', 'bank_name': 'Updated Bank'}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.bank_account.refresh_from_db()
        self.assertEqual(self.bank_account.account_number, '0987654321')
        self.assertEqual(self.bank_account.bank_name, 'Updated Bank')

    def test_delete_bank_account(self):
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BankAccount.objects.filter(id=self.bank_account.id).exists())