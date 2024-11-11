from rest_framework import serializers

from tutoring.models import Subject, Lesson, AvailableHour


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']


class LessonSerializer(serializers.ModelSerializer):
    tutor = serializers.StringRelatedField()
    student = serializers.StringRelatedField()
    subject = serializers.StringRelatedField()

    class Meta:
        model = Lesson
        fields = [
            'id', 'tutor', 'student', 'subject', 'start_time', 'end_time',
            'created_at', 'google_meet_url', 'rating', 'feedback'
        ]
        read_only_fields = ('created_at',)

class AvailableHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableHour
        fields = ['id', 'day_of_week', 'start_time', 'end_time']
        read_only_fields = ('id',)