from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView
from django.db import transaction
from core.models import RestaurantFoodCategory, RestaurantCuisine, Restaurant, FoodStyle, FoodMenu, FoodExtra, Category
from api.serializers.food import CategoryListSerializer, CategoryDetailSerializer, FoodMenuListSerializer, FoodDetailSerializer
from django.db.models import Q
from rest_framework.decorators import api_view


class AllCategoryListViewSet(ListAPIView):
    serializer_class = CategoryListSerializer
    model = Category
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        if self.request.query_params.get('search'):
            name = self.request.query_params.get('search', "")
            return self.model.objects.filter(name__icontains=name)
        return self.model.objects.all().distinct('name')

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class CategoryDetailViewSet(RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    model = Category
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, pk=self.kwargs.get('category_id'))

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class FoodListViewSet(ListAPIView):
    serializer_class = FoodMenuListSerializer
    model = FoodMenu
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        if "search" in self.request.query_params:
            search = self.request.query_params.get("search", "")
            return self.model.objects.filter(Q(restaurant__name__icontains=search) | Q(category__category__icontains=search) | Q(name__icontains=search))
        return self.model.objects.all()

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class FoodDetailViewSet(RetrieveAPIView):
    serializer_class = FoodDetailSerializer
    model = FoodMenu
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, pk=self.kwargs.get('food_id'))

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class TodaysDealViewSet(ListAPIView):
    serializer_class = FoodMenuListSerializer
    model = FoodMenu
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.all()

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class CategoryFoodListViewSet(ListAPIView):
    serializer_class = FoodMenuListSerializer
    model = FoodMenu
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        serializer_class = FoodMenuListSerializer
        kwargs['many'] = True
        return serializer_class(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        category = Category.objects.get(id=self.kwargs.get('category_id'))
        return self.model.objects.filter(main_category=category)

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
