
from rest_framework import serializers
from appaccount.models import User
# from rest_framework import permissions


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = [ 'id','username', 'email', 'groups',]
        # fields = '__all__'
