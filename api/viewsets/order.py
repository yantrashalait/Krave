from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView
from django.db import transaction
from core.models import Restaurant, FoodStyle, FoodMenu, FoodExtra, FoodCart, Order
from delivery.models import Delivery
from api.serializers.food import CategoryListSerializer, CategoryDetailSerializer, FoodMenuListSerializer
from api.serializers.order import CartSerializer, OrderCreateSerializer, CartListSerializer,\
    OrderListSerializer, OrderDetailSerializer
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from api.permissions import IsOwner, IsOwnerOrReadOnly
from core.views import randomString

from user.models import User

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
    serializer_class = CartListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return FoodCart.objects.filter(user=self.request.user, checked_out=False)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        try:
            delivery_charge = self.get_queryset()[0].restaurant.delivery_charge
        except:
            delivery_charge = 0.0

        # calculate sub_total for the cart
        sub_total = 0
        for item in self.get_queryset():
            sub_total += item.get_total
        # calculate total price of the order
        total_price = sub_total + delivery_charge

        return Response({
            'status': True,
            'data': {
                'cart': serializer.data,
                'delivery_charge': delivery_charge,
                'sub_total': sub_total,
                'total': total_price
                }
        }, status=status.HTTP_200_OK)


class CartEditViewSet(RetrieveUpdateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self, *args, **kwargs):
        cart = get_object_or_404(FoodCart, pk=self.kwargs.get("cart_id"))
        self.check_object_permissions(self.request, cart)
        return get_object_or_404(FoodCart, pk=self.kwargs.get("cart_id"))

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        quantity = serializer.validated_data.get('number_of_food', 1)
        cart = FoodCart.objects.get(id=self.kwargs.get("cart_id"))
        cart.number_of_food = quantity
        cart.save()
        return Response({
            'status': True,
            'msg': 'Updated successfully.'
        }, status=status.HTTP_200_OK)


class OrderPlaceViewSet(CreateAPIView):
    serializer_class = OrderCreateSerializer
    model = Order
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        order = Order()

        # get logged in user
        user = request.user
        note = validated_data.get("note", "")
        address_line1 = validated_data.get("address_line1", "")
        address_line2 = validated_data.get("address_line2", "")
        city = validated_data.get("city", "")
        state = validated_data.get("state", "")
        zip_code = validated_data.get("zip_code", "")
        payment = validated_data.get("payment", 1)

        # get total price from cart of user
        if not FoodCart.objects.filter(user=user, checked_out=False).exists():
            return Response({
                "status": False,
                "msg": "Order placement failed",
                "errors": {
                    "cart": ["Nothing in cart to place order."]
                }
            })
        total = 0
        for item in FoodCart.objects.filter(user=user, checked_out=False):
            total += item.get_total
            restaurant = item.restaurant
        total += restaurant.delivery_charge

        order.note = note
        order.address_line1 = address_line1
        order.address_line2 = address_line2
        order.city = city
        order.state = state
        order.zip_code = zip_code
        order.total_price = total
        order.payment = payment
        order.user = user

        order.paid = False

        last_order = Order.objects.last()
        if last_order:
            order_id = Order.objects.last().id
            order_id = order_id + 1
        else:
            order_id = 1

        id_string = randomString() + str(order_id)
        if Order.objects.filter(id_string=id_string).exists():
            id_string = randomString() + str(order_id)
        order.id_string = id_string
        order.status = 1
        order._runsignal = False
        order.save()

        for item in FoodCart.objects.filter(user=user, checked_out=False):
            order.cart.add(item)
            item.checked_out = True
            item.save()

        order._runsignal = True
        order.save()
        return Response({
            'status': True,
            'msg': 'Order placed successfully.'
        }, status=status.HTTP_200_OK)


class OrderListViewSet(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    model = Order

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(~Q(status=6), user=self.request.user)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class OrderDetailViewSet(RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    model = Order

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class OrderHistoryViewSet(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    model = Order

    def get_queryset(self, *args, **kwargs):
        assigned_orders = self.request.user.delivery.all()
        order_list = []
        for item in assigned_orders:
            if item.status == 1:
                order_list.append(item.order)
        return order_list

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class OrderOngoingHistoryViewSet(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    model = Order

    def get_queryset(self, *args, **kwargs):
        assigned_orders = self.request.user.delivery.all()
        order_list = []
        for item in assigned_orders:
            if item.status == 0:
                order_list.append(item.order)
        return order_list

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class EditOrderStatusViewSet(RetrieveUpdateAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    model = Delivery

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.get(order=self.kwargs.get("order_id"))

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        status = serializer.validated_data.get('status')
        delivery = self.get_queryset()
        order = delivery.order
        order.status = status
        order.save()

        return Response({
            'status': True,
            'msg': 'Updated successfully.'
        }, status=status.HTTP_200_OK)
