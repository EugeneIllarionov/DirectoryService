from collections import OrderedDict
from datetime import datetime

from rest_framework.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Directory, DirectoryBase
from .serializers import DirectoryItemSerializer, DirectorySerializer, DirectoryBaseSerializer


def pk_validation(pk):
    try:
        int_pk = int(pk)
        if int_pk > 0 and str(int_pk) == pk:
            return True
    except:
        raise ValidationError('id must be positive integer')


def date_validation(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        raise ValidationError("date must have '%Y-%m-%d' format")


class DirectoryPagination(PageNumberPagination):
    """
    custom paginator used for DirectoryView
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class DirectoryView(ViewSet):
    paginator = DirectoryPagination()

    def custom_response(self, data, request):
        """
        short version to get paginated response with status code 200 or 204
        :param serializer data:
        :param request:
        :return: Response with PageNumberPagination default field
        """
        if len(data) == 0:
            return Response(status=204)
        else:
            page = self.paginator.paginate_queryset(data, request)
            return self.paginator.get_paginated_response(page)

    def list(self, request):
        """
        :return directory list or directory list which are relevant on the specified date
        TODO: get queryset without loop
        """
        actual_on = self.request.query_params.get('actual_on')
        if actual_on is None:
            queryset = DirectoryBase.objects.all()
            serializer = DirectoryBaseSerializer(queryset, many=True)
        else:
            date_validation(actual_on)
            # queryset = Directory.objects.filter(directory_base__versions__start_date__lte=actual_on)
            queryset = Directory.objects.none()

            dirs = DirectoryBase.objects.all()
            for _dir in dirs:
                queryset |= _dir.versions.filter(start_date__lte=actual_on)[:1]
            serializer = DirectorySerializer(queryset, many=True)

        return self.custom_response(serializer.data, request)

    def retrieve(self, request, pk):
        """
        :return one directory item by primary key
        """
        pk_validation(pk)
        directory = get_object_or_404(DirectoryBase, pk=pk).current_directory()
        serializer = DirectorySerializer(directory)
        return Response(serializer.data)

    @action(detail=True)
    def items(self, request, pk):
        """
        :param request:
        :param pk:
        :return: directory items with filtering by version of directory, value and code of item
        """
        pk_validation(pk)
        version = self.request.query_params.get('version')
        value = self.request.query_params.get('value')
        code = self.request.query_params.get('code')

        if version is None:
            version = get_object_or_404(DirectoryBase, pk=pk).current_version()

        _dir = get_object_or_404(DirectoryBase, pk=pk).versions.filter(version=version).first()
        if _dir is None:
            raise Http404
        items = _dir.related_items

        if value is None and code is None:
            pass
        elif value is None:
            items = items.filter(code=code)
        elif code is None:
            items = items.filter(value=value)
        else:
            items = items.filter(value=value, code=code)

        serializer = DirectoryItemSerializer(items, many=True)

        return self.custom_response(serializer.data, request)
