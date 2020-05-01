from django.shortcuts import render, get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers_old import RestaurantListSerializer, RestaurantRequestSerializer, FoodMenuSerializer, RestaurantDetailSerializer, RestaurantFoodCategorySerializer, \
UserCartSerializer, CategorySerializer, CategorySingleSerializer, FoodMenuDetailSerializer
from core.models import Restaurant, RestaurantRequest, FoodMenu, RestaurantFoodCategory, FoodCart
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView
from django.contrib.auth.models import Group
from userrole.models import UserRole
from django.db import transaction
from user.models import UserProfile
import django_filters.rest_framework


class CategoryViewSet(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return RestaurantFoodCategory.objects.all().distinct()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        })

class CategorySingleViewSet(RetrieveAPIView):
    serializer_class = CategorySingleSerializer

    def get_object(self):
        return get_object_or_404(RestaurantFoodCategory, id=self.kwargs.get('category_id'))

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        })

class RestaurantFoodCategoryViewSet(ListCreateAPIView):
    serializer_class = RestaurantFoodCategorySerializer

    def get_queryset(self):
        return RestaurantFoodCategory.objects.filter(restaurant__id=self.kwargs.get('rest_id'))

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            })
        self.perform_create(serializer)
        return Response({
            'status': True,
            'msg': 'Category successfully assigned.',
            'data': serializer.data
        })


class RestaurantFoodCategorySingleViewSet(RetrieveUpdateAPIView):
    serializer_class = RestaurantFoodCategorySerializer

    def get_object(self):
        return RestaurantFoodCategory.objects.get(id=self.kwargs.get('category_id'))

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        })

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object, data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            })

        self.perform_update(serializer)
        return Response({
            'status': True,
            'msg': 'Updated successfully',
            'data': serializer.data
        })


class RestaurantListViewSet(ListAPIView):
    serializer_class = RestaurantListSerializer

    def get_queryset(self):
        if self.request.query_params.get('name'):
            name = self.request.query_params.get('name')
            return Restaurant.objects.filter(name__icontains=name).prefetch_related('food_category')
        return Restaurant.objects.all().prefetch_related('food_category')

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        })


class RestaurantSingleViewSet(RetrieveUpdateAPIView):
    serializer_class = RestaurantDetailSerializer

    def get_object(self):
        return Restaurant.objects.get(id=self.kwargs.get('rest_id'))

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            })

        self.perform_update(serializer)
        return Response({
            'status': True,
            'msg': 'Updated successfully',
            'data': serializer.data
        })


class RestaurantFoodListViewSet(ListAPIView):
    serializer_class = FoodMenuSerializer

    def get_queryset(self):
        return FoodMenu.objects.filter(restaurant_id=self.kwargs.get('rest_id'))

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        })


class FoodMenuSingleViewSet(RetrieveUpdateDestroyAPIView):
    serializer_class = FoodMenuDetailSerializer

    def get_object(self):
        return FoodMenu.objects.get(pk=self.kwargs.get('food_id'))

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            })
        self.perform_update(serializer)
        return Response({
            'status': True,
            'msg': 'Updated successfully.',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'status': True,
                'msg': 'Deleted Successfully.'
            })
        except Exception:
            return Response({
                'status': False,
                'msg': 'Failed to delete item.'
            })


class FoodSearch(ListAPIView):
    serializer_class = FoodMenuSerializer

    def get_queryset(self):
        if self.request.query_params.get('name', None):
            name = self.request.query_params.get('name')
            return FoodMenu.objects.filter(name__icontains=name)
        if self.request.query_params.get('category', None):
            category = self.request.query_params.get('category')
            return FoodMenu.objects.filter(category__name__icontains=category)
        return FoodMenu.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_queryset(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        })


# class RestaurantFoodCategoryListViewSet(ListCreateAPIView):
#     serializer_class = RestaurantFoodCategorySerializer

#     def get_queryset(self):
#         return RestaurantFoodCategory.objects.filter(restaurant__id=self.kwargs.get('pk'))





# class RestaurantDetailViewSet(RetrieveAPIView):
#     def get_object(self):
#         return Restaurant.objects.get(pk=self.kwargs.get('pk'))

#     def retrieve(self, request, *args, **kwargs):
#         serializer = RestaurantDetailSerializer(self.get_object())
#         serializer_data = serializer.data

#         meal_types = RestaurantMealType.objects.filter(restaurant__id=kwargs.get('pk'))
#         rest_meal_serializer = RestaurantDetailMealSerializer(meal_types)
#         serializer_data['meals'] = rest_meal_serializer.data

#         return Response(serializer_data)


class RestaurantRequestViewSet(viewsets.ModelViewSet):
    queryset = RestaurantRequest.objects.all()
    serializer_class = RestaurantRequestSerializer


class UserCartViewSet(ListCreateAPIView):
    serializer_class = UserCartSerializer

    def get_queryset(self):
        return FoodCart.objects.filter(user__id=self.kwargs.get('user_id'))

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        })

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            })
        self.perform_create(serializer)
        return Response({
            'status': True,
            'msg': 'Added to cart',
            'data': serializer.data
        })


class UserCartSingleViewSet(RetrieveUpdateDestroyAPIView):
    serializer_class = UserCartSerializer

    def get_object(self):
        return FoodCart.objects.get(id=self.kwargs.get('cart_id'))

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        })

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            })
        self.perform_update(serializer)
        return Response({
            'status': True,
            'msg': 'Successfully updated.',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'status': True,
                'msg': 'Deleted successfully.',
            })
        except Exception as e:
            return Response({
                'status': False,
                'msg': 'Failed to delete item.'
            })
