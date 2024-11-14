from rest_framework import serializers

from tutoring.choices import ROLE_CHOICES
from tutoring.exceptions.exceptions import DuplicateKeyException
from tutoring.models import User, Role


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    roles = serializers.ChoiceField(choices=ROLE_CHOICES, write_only=True)
    date_of_birth = serializers.DateField(required=False)

    class Meta:
        fields = ('username', 'first_name', 'last_name', 'password', 'roles', 'date_of_birth')
        write_only_fields = ('password', 'account_type')
        read_only_fields = ('id',)

    def create(self, validated_data):
        if User.objects.filter(username=validated_data['username']).exists():
            raise DuplicateKeyException('A user with this email already exists')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data.get('date_of_birth'),
            phone_number=validated_data.get('phone_number')
        )
        role_ids = Role.get_role_ids([validated_data['roles']])

        user.roles.add(role_ids[0])
        user.set_password(validated_data['password'])
        user.save()
        return user
