from rest_framework import serializers

from django.conf import settings
from weapon.membership.models import Membership, UserMembership, MembershipPayment


class MembershipSerializer(serializers.ModelSerializer):
    amount = serializers.ReadOnlyField()
    month_amount = serializers.ReadOnlyField()

    class Meta:
        model = Membership
        fields = "__all__"


class UserMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMembership
        depth = 2
        fields = "__all__"


class UserMembershipSerializerForPayment(serializers.ModelSerializer):
    class Meta:
        model = UserMembership
        fields = "__all__"


class MembershipPaymentSerializer(serializers.ModelSerializer):
    # user_membership = serializers.SerializerMethodField()
    # sale_code = serializers.SerializerMethodField()

    class Meta:
        model = MembershipPayment
        depth = 1
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MembershipPaymentSerializer, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].read_only = True

    # def get_user_membership(self, instance):
    #     user_membership_instance = UserMembership.objects.filter(membership_payment=instance.id).first()
    #     if not user_membership_instance:
    #         return None
    #     return UserMembershipSerializer(user_membership_instance).data


class MembershipPaymentForUserMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPayment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MembershipPaymentForUserMembershipSerializer, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].read_only = True


