
from rest_framework import serializers
from appaccount.models import User
# from appmarks.serializiers import StudentSerializer
# from rest_framework import permissions
# from appmarks.serializiers import ListTeacherSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name',
                  'gender', 'birthday', 'email', 'phone_number', 'address', 'is_teacher', ]


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
