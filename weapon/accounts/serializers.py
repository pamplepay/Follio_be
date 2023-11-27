from django.conf import settings

from rest_framework import serializers, permissions
from rest_framework.validators import UniqueValidator

from .models import PhoneNumber, Profile, RequestDeleteUser, RecommendUser


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    recommend_username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def validate_user(self, value):
        if self.context['request']._request.method not in permissions.SAFE_METHODS:
            unique = UniqueValidator(
                self.Meta.model.objects.all(),
                message='Profile with this user already exists.'
            )
            unique.set_context(self.fields['user'])
            unique(value)
        return value

    def get_recommend_username(self, instance):
        recommend_user = instance.user.recommend_user.all().first()
        if recommend_user:
            return recommend_user.recommend_user.username
        return None


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('phone_number', 'is_verified')
        read_only_fields = ("is_verified", )


class PhoneNumberVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True)
    code_by_phone_number = serializers.CharField(write_only=True)


class RequestDeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestDeleteUser
        fields = "__all__"


class RecommendUserSerializer(serializers.Serializer):
    class Meta:
        model = RecommendUser
        fields = "__all__"
