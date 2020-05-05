from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView
from django.db import transaction
from core.models import Restaurant, FoodStyle, FoodMenu, FoodExtra, FoodCart, Order
from api.serializers.food import CategoryListSerializer, CategoryDetailSerializer, FoodMenuListSerializer
from api.serializers.order import CartSerializer, OrderSerializer
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from api.permissions import IsOwner, IsOwnerOrReadOnly


class AddToCartViewSet(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        # get all extras
        extras = validated_data.pop('extras', [])
        # get logged in user
        user = request.user
        # get the restaurant
        restaurant = Restaurant.objects.get(id=validated_data.get('food').restaurant.id)
        cart = FoodCart.objects.create(user=user, restaurant=restaurant, **validated_data)
        for item in extras:
            cart.extras.add(item)
        
        return Response({
            'status': True,
            'msg': 'Added to cart'
        }, status=status.HTTP_200_OK)


class CartListViewSet(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return FoodCart.objects.filter(user=self.request.user, checked_out=False)
    
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
