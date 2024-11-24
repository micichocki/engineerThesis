from rest_framework import serializers

from tutoring.models import Subject, AvailableHour, EducationLevel, WorkingExperience, TutorSubjectPrice


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = ['id', 'level']
        read_only_fields = ('id',)

class AvailableHourSerializer(serializers.ModelSerializer):
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = AvailableHour
        fields = ['id', 'day_of_week', 'start_time', 'end_time']
        read_only_fields = ('id',)

    def get_start_time(self, obj):
        return obj.start_time.strftime('%H:%M')

    def get_end_time(self, obj):
        return obj.end_time.strftime('%H:%M')

class WorkingExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingExperience
        fields = ['id', 'position', 'start_date', 'end_date', 'description']
        read_only_fields = ('id',)

class TutorSubjectPriceSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    class Meta:
        model = TutorSubjectPrice
        fields = ['subject', 'price_min', 'price_max']

