from django.db import migrations

def add_popular_subjects(apps, schema_editor):
    Subject = apps.get_model('tutoring', 'Subject')
    popular_subjects = [
        'Mathematics',
        'English',
        'Science',
        'History',
        'Geography'
        'Chemistry',
        'Physics',
        'Biology',
        'Computer Science',
        'Art',
        'Music',
    ]
    for subject_name in popular_subjects:
        Subject.objects.create(name=subject_name)

class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0003_lesson_created_at_lesson_feedback_and_more'),
    ]

    operations = [
        migrations.RunPython(add_popular_subjects),
    ]