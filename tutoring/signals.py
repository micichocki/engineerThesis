from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import User, TutorProfile, StudentProfile, ParentProfile


@receiver(m2m_changed, sender=User.roles.through)
def create_role_profiles(sender, instance, action, **kwargs):
    if action == "post_add":
        if instance.roles.filter(name="Tutor").exists() and not hasattr(instance, 'tutorprofile'):
            TutorProfile.objects.create(user=instance)
        if instance.roles.filter(name="Student").exists() and not hasattr(instance, 'studentprofile'):
            StudentProfile.objects.create(user=instance)
        if instance.roles.filter(name="Parent").exists() and not hasattr(instance, 'parentprofile'):
            ParentProfile.objects.create(user=instance)

