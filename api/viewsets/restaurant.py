from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView
from django.db import transaction
from api.serializers.restaurant import RestaurantListSerializer, RestaurantDetailSerializer, RestaurantReviewSerializer, RestaurantRatingSerializer
from api.serializers.food import FoodMenuListSerializer
from core.models import Restaurant, FoodMenu, RestaurantReview, RestaurantRating
from rest_framework.decorators import api_view, permission_classes


class RestaurantListViewSet(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
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


class RestaurantFoodListViewSet(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FoodMenuListSerializer
    model = FoodMenu

    def get_queryset(self, *args, **kwargs):
        _rest_id = self.kwargs.get('rest_id')
        restaurant = get_object_or_404(Restaurant, pk=_rest_id)
        if "search" in self.request.query_params:
            search = self.request.query_params.get("search", "")
            return self.model.objects.filter(Q(restaurant__name__icontains=search) | Q(category__category__icontains=search) | Q(name__icontains=search), restaurant=restaurant)
        return self.model.objects.filter(restaurant=restaurant)

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class RestaurantPopularDishesViewSet(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FoodMenuListSerializer
    model = FoodMenu

    def get_queryset(self, *args, **kwargs):
        _rest_id = self.kwargs.get('rest_id')
        restaurant = get_object_or_404(Restaurant, pk=_rest_id)
        return self.model.objects.filter(restaurant=restaurant)

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class RestaurantReviewViewSet(ListCreateAPIView):
    serializer_class = RestaurantReviewSerializer
    model = RestaurantReview
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Restaurant, pk=self.kwargs.get('restaurant_id'))

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(restaurant=self.get_object())

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': 'Failed'
            }, status=status.HTTP_400_BAD_REQUEST)

        restaurant = self.get_object()
        user = request.user
        review = serializer.validated_data['review']
        self.model.objects.create(restaurant=restaurant, user=user, review=review)

        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class RestaurantRatingViewSet(ListCreateAPIView):
    serializer_class = RestaurantRatingSerializer
    model = RestaurantRating
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Restaurant, pk=self.kwargs.get('restaurant_id'))

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(restaurant=self.get_object())

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': 'Failed'
            }, status=status.HTTP_400_BAD_REQUEST)

        restaurant = self.get_object()
        user = request.user
        rating = serializer.validated_data['rating']
        self.model.objects.create(restaurant=restaurant, user=user, rating=rating)

        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
