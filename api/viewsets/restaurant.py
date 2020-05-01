from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView
from django.db import transaction
from api.serializers.restaurant import RestaurantListSerializer, RestaurantDetailSerializer
from core.models import Restaurant


class RestaurantListViewSet(ListAPIView):
    serializer_class = RestaurantListSerializer
    model = Restaurant

    def get_queryset(self, *args, **kwargs):
        if self.request.query_params.get('search'):
            name = self.request.query_params.get('search', "")
            return self.model.objects.filter(name__icontains=name)
        return self.model.objects.all()

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class RestaurantDetailViewSet(RetrieveAPIView):
    serializer_class = RestaurantDetailSerializer   
    model = Restaurant

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, pk=self.kwargs.get('rest_id'))
    
    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)