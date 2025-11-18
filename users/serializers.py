from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ParentProfile, ChildProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        ParentProfile.objects.create(user=user)
        return user


class ParentProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ParentProfile
        fields = ('id', 'user', 'phone', 'consent_given', 'consent_date', 'locale')


class ChildProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildProfile
        fields = ('id', 'parent', 'first_name', 'last_name', 'dob', 'gender', 'grade', 'avatar_url', 'notes')
        read_only_fields = ('parent',)
