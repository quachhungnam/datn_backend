
from rest_framework import serializers
from appaccount.models import User
# from rest_framework import permissions


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = [ 'id','username', 'email', 'groups',]
        # fields = '__all__'



class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)