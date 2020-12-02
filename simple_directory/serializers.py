from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import DirectoryItem, Directory, DirectoryBase


class DirectoryBaseSerializer(ModelSerializer):

    version_count = serializers.IntegerField(source='versions.count')

    class Meta:
        model = DirectoryBase
        fields = ['id', 'name', 'short_name', 'description', 'last_version', 'current_version', 'version_count']


class DirectorySerializer(ModelSerializer):

    id = serializers.CharField(source='directory_base.id')
    name = serializers.CharField(source='directory_base.name')
    short_name = serializers.CharField(source='directory_base.short_name')
    description = serializers.CharField(source='directory_base.description')

    class Meta:
        model = Directory
        fields = ('id', 'name', 'short_name', 'description', 'version', 'start_date')


class DirectoryItemSerializer(ModelSerializer):

    class Meta:
        model = DirectoryItem
        fields = ('code', 'value')
