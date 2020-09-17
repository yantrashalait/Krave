import datetime

from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView

from core.models import RestaurantFoodCategory, RestaurantCuisine, Restaurant, FoodStyle, FoodMenu, FoodExtra, \
    Category, FoodReview, FoodRating
from api.serializers.food import CategoryListSerializer, CategoryDetailSerializer, FoodMenuListSerializer, \
    FoodDetailSerializer, FoodExtraSerializer, FoodStyleSerializer, FoodReviewSerializer, FoodRatingSerializer
from user.models import UserFavourite

from ..utils import trending_foods


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
            return self.model.objects.filter(
                Q(restaurant__name__icontains=search) |
                Q(main_category__name__icontains=search) |
                Q(name__icontains=search))
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

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Category, id=self.kwargs.get('category_id'))

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(main_category=self.get_object())

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class FoodExtraDetailViewSet(ListAPIView):
    serializer_class = FoodExtraSerializer
    model = FoodExtra
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        return get_object_or_404(FoodMenu, pk=self.kwargs.get('food_id'))

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(food=self.get_object())

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data,
        }, status=status.HTTP_200_OK)


class FoodStyleDetailViewSet(ListAPIView):
    serializer_class = FoodStyleSerializer
    model = FoodStyle
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        return get_object_or_404(FoodMenu, pk=self.kwargs.get('food_id'))

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(food=self.get_object())

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data,
        }, status=status.HTTP_200_OK)


class FoodReviewViewSet(ListAPIView):
    serializer_class = FoodReviewSerializer
    model = FoodReview

    def get_object(self, *args, **kwargs):
        return get_object_or_404(FoodMenu, pk=self.kwargs.get('food_id'))

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(food=self.get_object())

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data,
        }, status=status.HTTP_200_OK)


class FoodReviewPostViewSet(CreateAPIView):
    serializer_class = FoodReviewSerializer
    model = FoodReview
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        return get_object_or_404(FoodMenu, pk=self.kwargs.get('food_id'))

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': 'Failed'
            }, status=status.HTTP_400_BAD_REQUEST)

        food = self.get_object()
        user = request.user
        review = serializer.validated_data['review']
        self.model.objects.create(food=food, user=user, review=review)

        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class FoodRatingViewSet(ListAPIView):
    serializer_class = FoodRatingSerializer
    model = FoodRating

    def get_object(self, *args, **kwargs):
        return get_object_or_404(FoodMenu, pk=self.kwargs.get('food_id'))

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(food=self.get_object())

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data,
        }, status=status.HTTP_200_OK)


class FoodRatingPostViewSet(CreateAPIView):
    serializer_class = FoodRatingSerializer
    model = FoodRating
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        return get_object_or_404(FoodMenu, pk=self.kwargs.get('food_id'))

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': 'Failed'
            }, status=status.HTTP_400_BAD_REQUEST)

        food = self.get_object()
        user = request.user
        rating = serializer.validated_data['rating']
        self.model.objects.create(food=food, user=user, rating=rating)

        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class TrendingFoodListVS(ListAPIView):
    serializer_class = FoodMenuListSerializer
    model = FoodMenu
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self, *args, **kwargs):
        return trending_foods()

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data[:10]
        }, status=status.HTTP_200_OK)


class UserFavouriteVS(ListCreateAPIView):
    serializer_class = FoodMenuListSerializer
    model = UserFavourite
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self, *args, **kwargs):
        return FoodMenu.objects.filter(favourites__deleted=False, favourites__user=self.request.user)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def add_to_favourite(request, food_id):
    try:
        food = FoodMenu.objects.get(id=food_id)
    except FoodMenu.DoesNotExist:
        return Response({
            'status': False,
            'msg': 'This food no longer exists in the system.'
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        favourite = UserFavourite.objects.get(user=request.user, food=food)
        if favourite.deleted:
            favourite.deleted = False
            favourite.save()
            return Response({
                "status": True,
                "msg": "Added to favourite."
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": False,
                "msg": "This food already exists in your favourites."
            }, status=status.HTTP_200_OK)
    except UserFavourite.DoesNotExist:
        UserFavourite.objects.create(user=request.user, food=food)
        return Response({
            "status": True,
            "msg": "Added to favourite."
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def delete_favourite(request, food_id):
    try:
        food = FoodMenu.objects.get(id=food_id)
    except FoodMenu.DoesNotExist:
        return Response({
            'status': False,
            'msg': 'This food no longer exists in the system.'
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        favourite = UserFavourite.objects.get(user=request.user, food=food)
    except UserFavourite.DoesNotExist:
        return Response({
            'status': False,
            'msg': 'You have not added this food to your favourite'
        })
    favourite.deleted = True
    favourite.deleted_at = datetime.datetime.now()
    favourite.save()
    return Response({
        'status': True,
        'msg': 'Removed food from favourite.'
    }, status=status.HTTP_200_OK)