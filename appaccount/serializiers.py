
from rest_framework import serializers
from appaccount.models import User
# from appmarks.serializiers import StudentSerializer
# from rest_framework import permissions
# from appmarks.serializiers import ListTeacherSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_teacher', 'first_name', 'last_name',
                  'gender', 'birthday', 'email', 'phone_number', 'address',  'password','avatar']
        read_only_fields = ('id', 'username', 'is_teacher', 'first_name', 'last_name',
                            'gender', 'birthday','avatar')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            # password=validated_data['[password']d
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
