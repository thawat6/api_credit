from rest_framework import routers, serializers, viewsets, generics, status, mixins
from data_api.models import UnitOfMeasureCategory, UnitOfMeasure, Dimension, Product, Coord, TimeWindow, OrderItem, InventoryItem, Location, CarrierClass, Carrier, Customer, Order, MapOutWay, MapWay, Map, Trip, UserProfile
from data_api.serializers import ProductSerializer, ProductCreateSerializer, UnitOfMeasureCategorySerializer, \
    UnitOfMeasureSerializer, DimensionSerializer, CoordSerializer, SetUserPassword,\
    TimeWindowSerializer, OrderItemSerializer, InventoryItemSerializer, \
    LocationSerializer, CarrierClassSerializer, CarrierSerializer, CustomerSerializer, \
    OrderSerializer, MapOutWaySerializer, MapWaySerializer, MapSerializer, TripSerializer, \
    DimensionCreateSerializer, OrderItemCreateSerializer, LocationCreateSerializer, \
    LocationNameSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer, OrderSimpleSerializer, CarrierClassCreateSerializer, \
    CarrierCreateSerializer, UserSerializer, TripCreateSerializer, UnitOfMeasureCreateSerializer, \
    UserDetailsSerializer, MapDetailSerializer, MapWayDetailSerializer, MapWayDetailCreateSerializer, \
    MapWayDetailUpdateSerializer, MapOutWayDetailCreateSerializer, MapOutWayDetailSerializer, \
    MapDetailCreateSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
import coreapi
from urllib.request import urlopen
import json
import traceback
import numpy as np
from django.http import HttpResponseNotFound
import operator
import locale

import requests


@api_view(['PATCH'])
def set_user_password(request, pk):
    if request.data['password'] != request.data['confirm_password']:
        return Response({'detail': 'Password and confirm paswword not match'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = SetUserPassword(user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in [
                'GET',
        ]:
            return UserDetailsSerializer
        return UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Product.objects.filter(
            created_user=None) | Product.objects.filter(
                created_user_id=1) | Product.objects.filter(
                    created_user__user_profile__company=self.request.user.
                    user_profile.company)

    # queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name', )

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return ProductCreateSerializer
        return ProductSerializer


class UnitOfMeasureCategoryViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasureCategory.objects.all()
    serializer_class = UnitOfMeasureCategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    http_method_names = ['get', 'head', 'options']
    search_fields = ('name', )


class UnitOfMeasureViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasure.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    http_method_names = [
        'get', 'post', 'head', 'put', 'patch', 'delete', 'options'
    ]
    filter_fields = ('category', )
    search_fields = ('name', )

    def retrieve_by_name(self, request, pk=None):
        uom = None
        if pk:
            try:
                if pk.isdigit():  # pk
                    uom = UnitOfMeasure.objects.get(pk=pk)
                else:
                    uom = UnitOfMeasure.objects.get(name=str(pk))
            except UnitOfMeasure.DoesNotExist:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
        serializer = UnitOfMeasureSerializer(uom)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return UnitOfMeasureCreateSerializer
        return UnitOfMeasureSerializer


class DimensionViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Dimension.objects.filter(
            created_user=None) | Dimension.objects.filter(
                created_user_id=1) | Dimension.objects.filter(
                    created_user__user_profile__company=self.request.user.
                    user_profile.company)

    # queryset = Dimension.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    http_method_names = [
        'get', 'post', 'head', 'put', 'patch', 'delete', 'options'
    ]
    search_fields = ('uom', )

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return DimensionCreateSerializer
        return DimensionSerializer


class CoordViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Coord.objects.filter(created_user=None) | Coord.objects.filter(
            created_user__user_profile__company=self.request.user.user_profile.
            company)

    # queryset = Coord.objects.all()
    serializer_class = CoordSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    http_method_names = [
        'get', 'post', 'head', 'put', 'patch', 'delete', 'options'
    ]


class TimeWindowViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return TimeWindow.objects.filter(
            created_user=None) | TimeWindow.objects.filter(
                created_user_id=1) | TimeWindow.objects.filter(
                    created_user__user_profile__company=self.request.user.
                    user_profile.company)

    # queryset = TimeWindow.objects.all()
    serializer_class = TimeWindowSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('begin', 'end')
    http_method_names = [
        'get', 'post', 'head', 'put', 'patch', 'delete', 'options'
    ]


class OrderItemViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return OrderItem.objects.filter(
            created_user=None) | OrderItem.objects.filter(
                created_user_id=1) | OrderItem.objects.filter(
                    created_user__user_profile__company=self.request.user.
                    user_profile.company)

    # queryset = OrderItem.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('product__name', 'product__id')
    http_method_names = [
        'get', 'post', 'head', 'put', 'patch', 'delete', 'options'
    ]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return OrderItemCreateSerializer
        return OrderItemSerializer


class InventoryItemViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return InventoryItem.objects.filter(
            created_user=None) | InventoryItem.objects.filter(
                created_user_id=1) | InventoryItem.objects.filter(
                    created_user__user_profile__company=self.request.user.
                    user_profile.company)

    # queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('product__name', 'product__id')
    http_method_names = [
        'get', 'post', 'head', 'put', 'patch', 'delete', 'options'
    ]


class LocationViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Location.objects.filter(
            created_user=None) | Location.objects.filter(
                created_user_id=1) | Location.objects.filter(
                    created_user__user_profile__company=self.request.user.
                    user_profile.company)

    # queryset = Location.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    http_method_names = [
        'get', 'post', 'head', 'put', 'patch', 'delete', 'options'
    ]
    filter_fields = ('location_type', )

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return LocationCreateSerializer
        return LocationSerializer


class LocationInstanceItemViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        queryset = Location.objects.filter(
            created_user=None) | Location.objects.filter(
                created_user_id=1) | Location.objects.filter(
                    created_user__user_profile__company=self.request.user.
                    user_profile.company)
        location_id = self.request.query_params.get('location_id', None)

        if location_id is not None:
            queryset = queryset.location_items
        return queryset

    def get_serializer_class(self):
        return LocationSerializer


class CarrierClassViewSet(viewsets.ModelViewSet):
    serializer_class = CarrierClassSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('carrier_type', )
    http_method_names = [
        'get', 'post', 'head', 'put', 'patch', 'delete', 'options'
    ]

    def get_queryset(self):
        carrier_type = self.kwargs.get('carrier_type', None)

        q = CarrierClass.objects.distinct()
        if carrier_type:
            q = q.filter(carrier_type=carrier_type)
            q = q.filter(created_user_id=1) | q.filter(
                created_user__user_profile__company=self.request.user.
                user_profile.company)
        return q

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CarrierClassCreateSerializer
        return CarrierClassSerializer

    def retrieve_by_name(self, request, pk=None):
        carrier_class = None
        carrier_type = pk
        if carrier_type:
            try:
                if carrier_type.isdigit():  # pk
                    carrier_class = CarrierClass.objects.get(pk=carrier_type)
                else:
                    carrier_class = CarrierClass.objects.get(
                        carrier_type=carrier_type)
            except CarrierClass.DoesNotExist:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
        serializer = CarrierClassSerializer(carrier_class)
        return Response(serializer.data)


class CarrierViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Carrier.objects.filter(
            created_user=None) | Carrier.objects.filter(
                created_user_id=1) | Carrier.objects.filter(
                    created_user__user_profile__company=self.request.user.
                    user_profile.company)

    # queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    http_method_names = [
        'get', 'post', 'head', 'put', 'patch', 'delete', 'options'
    ]
    search_fields = ('name', 'carrier_class__carrier_type', 'driver')
    filter_fields = ('carrier_class', 'id',
                     'is_occupied', 'location', 'driver')

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CarrierCreateSerializer
        return CarrierSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Customer.objects.filter(
            created_user=None) | Customer.objects.filter(
                created_user_id=1) | Customer.objects.filter(
                    created_user__user_profile__company=self.request.user.
                    user_profile.company)

    # queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name', 'address', 'phone', 'mobile')


class OrderViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Order.objects.filter(created_user=None) | Order.objects.filter(
            created_user_id=1) | Order.objects.filter(
                created_user__user_profile__company=self.request.user.
                user_profile.company)

    # queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('id', 'delivery_date', 'customer__name', 'order_type',
                     'status', 'source_location__name',
                     'delivery_location__name')
    ordering_fields = ('sequence', 'delivery_date')
    filter_fields = ('status', 'source_location', 'delivery_location',
                     'delivery_time_windows', 'order_type', 'customer')

    def retrieve_items(self, request, order_id=None):
        if order_id:
            try:
                order = Order.objects.get(pk=order_id)
                serializer = OrderItemSerializer(order.items, many=True)
                return Response(serializer.data)
            except Order.DoesNotExist:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
        serializer = CarrierClassSerializer(carrier_class)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method in [
                'POST',
        ]:
            return OrderCreateSerializer
        if self.request.method in [
                'PUT',
                'PATCH',
        ]:
            return OrderStatusUpdateSerializer
        return OrderSerializer


class OrderInstanceItemViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('product__name', 'product__id')
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        order_id = self.kwargs.get('order_id', None)
        if order_id is not None:
            queryset = OrderItem.objects.filter(
                created_user=None,
                item_orders=order_id) | OrderItem.objects.filter(
                    created_user_id=1,
                    item_orders=order_id) | OrderItem.objects.filter(
                        created_user__user_profile__company=self.request.user.
                        user_profile.company,
                        item_orders=order_id)
        else:
            queryset = OrderItem.objects.filter(
                created_user=None) | OrderItem.objects.filter(
                    created_user_id=1) | OrderItem.objects.filter(
                        created_user__user_profile__company=self.request.user.
                        user_profile.company)
        return queryset

    def get_serializer_class(self):
        return OrderItemSerializer


class OrderInstanceLocationViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        queryset = Location.objects.all()
        order_id = self.request.query_params.get('order_id', None)
        if order_id is not None:
            queryset = queryset.item_orders
        return queryset

    def get_serializer_class(self):
        return LocationNameSerializer


class MapOutWayViewSet(viewsets.ModelViewSet):

    # def get_queryset(self):
    #     return MapOutWay.objects.filter(created_user__user_profile__company=self.request.user.user_profile.company)

    queryset = MapOutWay.objects.all()
    serializer_class = MapOutWaySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)


class MapWayViewSet(viewsets.ModelViewSet):

    # def get_queryset(self):
    #     return MapWay.objects.filter(created_user__user_profile__company=self.request.user.user_profile.company)

    queryset = MapWay.objects.all()
    serializer_class = MapWaySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    #filter_fields = ('output_location','distance','duration')


class MapViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Map.objects.filter(created_user=None) | Map.objects.filter(
            created_user_id=1) | Map.objects.filter(
                created_user__user_profile__company=self.request.user.
                user_profile.company)

    # queryset = Map.objects.all()
    serializer_class = MapSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)


class MapOutWayDetailViewSet(viewsets.ModelViewSet):

    # def get_queryset(self):
    #     return MapOutWay.objects.filter(created_user__user_profile__company=self.request.user.user_profile.company)

    queryset = MapOutWay.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return MapOutWayDetailCreateSerializer
        return MapOutWayDetailSerializer


class MapWayDetailViewSet(viewsets.ModelViewSet):

    # def get_queryset(self):
    #     return MapWay.objects.filter(created_user__user_profile__company=self.request.user.user_profile.company)

    queryset = MapWay.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    #filter_fields = ('output_location','distance','duration')

    def destroy(self, request, pk=None):
        try:
            mapway = MapWay.objects.get(pk=pk)
        except Exception as e:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        output_ways = MapOutWay.objects.filter(mapway=pk)

        for output_way in output_ways:
            output_way.delete()

        mapway.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MapWayDetailCreateSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return MapWayDetailUpdateSerializer
        return MapWayDetailSerializer


class MapDetailViewSet(viewsets.ModelViewSet):

    # def get_queryset(self):
    #     return Map.objects.filter(created_user__user_profile__company=self.request.user.user_profile.company)

    queryset = Map.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return MapDetailCreateSerializer
        return MapDetailSerializer


class TripViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Trip.objects.filter(created_user=None) | Trip.objects.filter(
            created_user_id=1) | Trip.objects.filter(
                created_user__user_profile__company=self.request.user.
                user_profile.company)

    # queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('delivery_date', 'source_location', 'carrier__driver')
    search_fields = (
        'name',
        'delivery_date',
        'carrier'
    )
    ordering_fields = ('delivery_date', 'carrier')

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TripCreateSerializer
        return TripSerializer


class TripInstanceOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSimpleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('id', 'delivery_date', 'customer__name', 'order_type',
                     'delivery_location__name')
    ordering_fields = ('sequence', 'delivery_date')
    filter_fields = ('delivery_location', 'delivery_time_windows',
                     'order_type', 'customer')

    def get_queryset(self):
        trip_id = self.kwargs.get('trip_id', None)
        if trip_id is not None:
            queryset = Order.objects.filter(
                trip_orders=trip_id, created_user=None) | Order.objects.filter(
                    trip_orders=trip_id,
                    created_user_id=1) | Order.objects.filter(
                        trip_orders=trip_id,
                        created_user__user_profile__company=self.request.user.
                        user_profile.company)
        else:
            queryset = Order.objects.filter(
                created_user=None) | Order.objects.filter(
                    created_user_id=1) | Order.objects.filter(
                        created_user__user_profile__company=self.request.user.
                        user_profile.company)
        return queryset


class TripInstanceCarrierClassViewSet(viewsets.ModelViewSet):
    serializer_class = CarrierClassSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = (
        'id',
        'carrier_type',
    )
    ordering_fields = ('carrier_type', )
    filter_fields = ('carrier_type', )

    def get_queryset(self):
        trip_id = self.kwargs.get('trip_id', None)
        if trip_id is not None:
            queryset = CarrierClass.objects.filter(
                trip_carrier_classes=trip_id)
        else:
            queryset = CarrierClass.objects.all()
        return queryset


def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2)


def get_plan(trip):
    plan = []
    location = []
    coords = []
    nodes = []
    location.append({
        'name': trip.source_location.name,
        'coord': trip.source_location.coord
    })
    lonlat = str(trip.source_location.coord.lon) + ',' + str(
        trip.source_location.coord.lat)
    nodes.append((float(trip.source_location.coord.lon),
                  float(trip.source_location.coord.lat)))
    coords.append(lonlat)

    # location.append({'name': trip.destination_location.name,'coord':trip.source_location.coord})
    # lonlat = str(trip.destination_location.coord.lon) + ','+ str(trip.destination_location.coord.lat)
    # nodes.append((float(trip.destination_location.coord.lon),float(trip.destination_location.coord.lat)))
    # coords.append(lonlat)

    total_weight = 0.0
    total_volume = 0.0

    for order in trip.orders.all():
        # order dimension calculation
        for order_item in order.items.all():
            total_weight += (order_item.product.weight * order_item.quantity)
            volume = order_item.product.dimension.width * \
                order_item.product.dimension.height * order_item.product.dimension.length
            total_volume += (volume * order_item.quantity)

        # order locations calculation
        coord = order.delivery_location.coord
        lonlat = str(coord.lon) + ',' + str(coord.lat)
        nodes.append((float(coord.lon), float(coord.lat)))
        coords.append(lonlat)
        location.append({
            'name': order.delivery_location.name,
            'coord': trip.source_location.coord
        })

    # vehicle estimation
    vehicles = []
    carrier_classes = {}
    for carrier_class in CarrierClass.objects.filter(
            trip_carrier_classes=trip.id):
        carrier_classes[carrier_class.id] = round(
            carrier_class.dimension.width * carrier_class.dimension.height *
            carrier_class.dimension.length * 0.9, 4)

    sorted_carrier_class = sorted(carrier_classes.items(),
                                  key=operator.itemgetter(1))[::-1]

    vehicles = []
    remain_volume = total_volume
    for vehicle in sorted_carrier_class:
        if remain_volume / (vehicle[1] * 1.0) > 0.0:
            remain_volume = remain_volume % (vehicle[1] * 1.0)
            used_vehicle = round(remain_volume / vehicle[1])
            vehicles.append((vehicle[0], used_vehicle))

    total_distance = 0.0
    total_duration = 0.0
    try:
        url = settings.OSRM_API_URL + 'trip/v1/driving/' + ';'.join(coords)
        response = urlopen(url).read()
        data = json.loads(str(response, 'utf-8'))
        plan_trip_costs = []
        for plan_trip in data['trips']:
            total_distance = plan_trip['distance']
            total_duration = plan_trip['duration']
            for leg in plan_trip['legs']:
                plan_trip_costs.append({
                    'distance': leg['distance'],
                    'duration': leg['duration']
                })
        # waypoints
        index = 1
        for waypoint in data['waypoints']:
            location_key = str(waypoint['location'][0]) + ',' + str(
                waypoint['location'][1])
            node_id = closest_node(
                (waypoint['location'][0], waypoint['location'][1]), nodes)
            plan.append({
                'index': index,
                'location': location[node_id],
                'cost': plan_trip_costs[node_id]
            })
            index += 1
    except:
        print('Error while call trip service')
        traceback.print_exc()
    return {
        'total_distance': total_distance,
        'total_duration': total_duration,
        'total_weight': total_weight,
        'total_volume': total_volume,
        'vehicles': vehicles,
        'way_plan': plan
    }


def get_all_cost(plan):
    calculated_cost = {}
    divider = {
        'distance': 1000,
        'trip': 1,
        'day': 1440,
        'week': 10080,
        'month': 43200,
        'year': 525600,
    }

    available_vehicle_types = [
        plan_vehicle[0] for plan_vehicle in plan['vehicles']
        if plan_vehicle[1] > 0
    ]

    for vehicle_type in available_vehicle_types:
        tmp_vehicle_type_cost = {}

        cost = 0

        for carrier in Carrier.objects.filter(carrier_class=vehicle_type):
            cost = float(plan['total_distance']) / float(
                divider[carrier.fuel_cost_type]) * float(carrier.fuel_cost)
            cost += float(carrier.service_cost) / float(
                divider[carrier.service_cost_type]) * float(
                    plan['total_duration'])
            cost += float(carrier.fixed_cost) / float(
                divider[carrier.fixed_cost_type]) * float(
                    plan['total_duration'])
            cost += float(carrier.man_cost) / float(
                divider[carrier.man_cost_type]) * float(plan['total_duration'])

            tmp_vehicle_type_cost[carrier.id] = cost

        if len(tmp_vehicle_type_cost) > 0:
            calculated_cost[vehicle_type] = tmp_vehicle_type_cost

    return calculated_cost


@login_required(login_url='/vrp/api/')
def exports_trip_detail(request, trip_id, format_param):
    try:
        trip = Trip.objects.get(pk=trip_id)
    except Trip.DoesNotExist:
        return HttpResponseNotFound('Not Found')

    response = HttpResponse(content_type='text/txt')
    #response['Content-Disposition'] = 'attachment; filename="' + trip.name.replace(' ','_') + '.txt"'

    response.write('Trip Name: ' + trip.name + '\n')

    response.write('Delivery Date: ' + str(trip.delivery_date) + '\n')
    response.write('Source Location: ' + str(trip.source_location.name) + '\n')
    # response.write('Destination Location: ' + str(trip.destination_location) + '\n')
    response.write('\n')
    plan = get_plan(trip)

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    response.write('Total weight: ' +
                   locale.format("%d", plan['total_weight'], grouping=True) +
                   ' kg\n')
    response.write('Total volume: ' +
                   locale.format("%d", plan['total_volume'], grouping=True) +
                   ' cbm\n')
    response.write('Total distance: ' +
                   locale.format("%d", plan['total_distance'], grouping=True) +
                   ' m\n')
    response.write('Total duration: ' +
                   locale.format("%d", plan['total_duration'], grouping=True) +
                   ' min(s)\n')
    response.write('\n')

    response.write('Vehicle usage: ' + '\n')
    for vehicle in plan['vehicles']:
        if vehicle[1] > 0:
            carrier_class = CarrierClass.objects.get(pk=vehicle[0])
            response.write('Carrier class: ' + carrier_class.carrier_type +
                           ' amount: ' + str(vehicle[1]) + '\n')
    response.write('\n')

    # get cost from not occupied carrier

    all_cost = get_all_cost(plan)
    total_suggested_vehicle_cost = 0

    response.write('Suggested Vehicle:\n')

    for vehicle_type in all_cost:
        minimum = {
            'carrier_id':
            list(all_cost[vehicle_type].keys())[0],
            'cost':
            float(all_cost[vehicle_type][list(
                all_cost[vehicle_type].keys())[0]])
        }

        for carrier_id in all_cost[vehicle_type]:
            if all_cost[vehicle_type][carrier_id] < minimum['cost']:
                minimum['carrier_id'] = carrier_id
                minimum['cost'] = all_cost[vehicle_type][carrier_id]

        costless_carrier = Carrier.objects.get(pk=minimum['carrier_id'])

        response.write('%s: %s (Cost: %.2f)\n' %
                       (costless_carrier.carrier_class.carrier_type,
                        costless_carrier, minimum['cost']))

        total_suggested_vehicle_cost += minimum['cost']

    response.write('\n')
    response.write('Total Suggested Vehicle Cost: %.2f\n' %
                   total_suggested_vehicle_cost)
    response.write('\n')

    response.write('Trip Plan: ' + '\n')
    for way in plan['way_plan']:
        response.write('Step: ' + str(way['index']) + '\n')
        response.write('Location Name: ' + way['location']['name'] + '\n')
        response.write('Location coord: ' + str(way['location']['coord'].lon) +
                       ',' + str(way['location']['coord'].lat) + '\n')
        response.write('Distance: ' + str(way['cost']['distance']) + '\n')
        response.write('Location Name: ' + str(way['cost']['duration']) + '\n')
        response.write('\n')

    return response


@api_view(['GET'])
def exports_plan_detail_api(request, trip_id, format_param):
    try:
        trip = Trip.objects.get(pk=trip_id)
    except Trip.DoesNotExist:
        return Response({'detail': 'Not found.'},
                        status=status.HTTP_404_NOT_FOUND)

    data = 'Trip Name: ' + trip.name + '\n'
    data += 'Delivery Date: ' + str(trip.delivery_date) + '\n'
    data += 'Source Location: ' + str(trip.source_location.name) + '\n'
    data += '\n'

    plan_data = json.loads(trip.plan_data or '[]')

    if (not len(plan_data)):
        return Response({'detail': data}, status=status.HTTP_200_OK)

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    data += 'Total cost: ' + locale.format(
        "%d", plan_data[0][0]['total_cost'], grouping=True) + ' baht\n'
    # response.write('Total weight: ' + locale.format("%d", plan['total_weight'], grouping=True) + ' kg\n')
    # response.write('Total volume: ' + locale.format("%d", plan['total_volume'], grouping=True) + ' cbm\n')
    data += 'Total distance: ' + locale.format(
        "%d", plan_data[0][0]['total_distance']['quantity'],
        grouping=True) + ' km\n'
    data += 'Total duration: ' + locale.format(
        "%s", plan_data[0][0]['total_time'], grouping=True) + ' hour(s)\n'
    data += '\n'

    data += 'Vehicle usage: ' + '\n'
    carrier = Carrier.objects.get(pk=plan_data[0][0]['carrier']['id'])
    data += str(carrier) + '\n'
    data += '\n'

    data += 'Trip Plan: ' + '\n'
    for stop in plan_data[0][0]['stops']:
        data += 'Step: ' + str(stop['seq']) + '\n'
        if stop['actions']:
            data += 'Action: ' + str(stop['actions'][0]['action']) + '\n'
            data += 'Order ID: ' + str(
                stop['actions'][0]['order']['id']) + '\n'
        data += 'Location Name: ' + stop['location']['name'] + '\n'
        data += 'Location coord: ' + str(
            stop['location']['coord']['lon']) + ',' + str(
                stop['location']['coord']['lat']) + '\n'
        data += 'Distance: ' + str(
            stop['costs']['distance']['quantity']) + ' ' + str(
                stop['costs']['distance']['uom']) + '\n'
        data += 'Duration: ' + str(stop['costs']['duration']) + '\n'
        data += 'Schedule Arrive: ' + str(
            stop['sched_arrive']['date']) + ' ' + str(
                stop['sched_arrive']['time']) + '\n'
        data += 'Schedule Depart: ' + str(
            stop['sched_depart']['date']) + ' ' + str(
                stop['sched_depart']['time']) + '\n'

        if 'items' in stop['location']:
            data += 'Items:\n'
            item_cnt = 1
            for item in stop['location']['items']:
                data += str(item_cnt) + '. ' + str(
                    Product.objects.get(
                        pk=item['product']['id']).name) + ' จำนวน ' + str(
                            item['quantity']) + ' ' + str(item['uom']) + '\n'
                item_cnt += 1

        data += '\n'

    return Response({'detail': data}, status=status.HTTP_200_OK)


# @login_required(login_url='/vrp/api/rest-auth/login/')
def exports_plan_detail(request, trip_id, format_param):

    try:
        trip = Trip.objects.get(pk=trip_id)
    except Trip.DoesNotExist:
        return HttpResponseNotFound('Not Found')

    response = HttpResponse(content_type='text/txt')

    response.write('Trip Name: ' + trip.name + '\n')

    response.write('Delivery Date: ' + str(trip.delivery_date) + '\n')
    response.write('Source Location: ' + str(trip.source_location.name) + '\n')
    response.write('\n')

    plan_data = json.loads(trip.plan_data or '[]')

    if (not len(plan_data)):
        return response

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    response.write(
        'Total cost: ' +
        locale.format("%d", plan_data[0][0]['total_cost'], grouping=True) +
        ' baht\n')
    # response.write('Total weight: ' + locale.format("%d", plan['total_weight'], grouping=True) + ' kg\n')
    # response.write('Total volume: ' + locale.format("%d", plan['total_volume'], grouping=True) + ' cbm\n')
    response.write('Total distance: ' + locale.format(
        "%d", plan_data[0][0]['total_distance']['quantity'], grouping=True) +
        ' km\n')
    response.write(
        'Total duration: ' +
        locale.format("%s", plan_data[0][0]['total_time'], grouping=True) +
        ' hour(s)\n')
    response.write('\n')

    response.write('Vehicle usage: ' + '\n')
    carrier = Carrier.objects.get(pk=plan_data[0][0]['carrier']['id'])
    response.write(str(carrier) + '\n')
    response.write('\n')

    response.write('Trip Plan: ' + '\n')
    for stop in plan_data[0][0]['stops']:
        response.write('Step: ' + str(stop['seq']) + '\n')
        response.write('Location Name: ' + stop['location']['name'] + '\n')
        response.write('Location coord: ' +
                       str(stop['location']['coord']['lon']) + ',' +
                       str(stop['location']['coord']['lat']) + '\n')
        response.write('Distance: ' +
                       str(stop['costs']['distance']['quantity']) + ' ' +
                       str(stop['costs']['distance']['uom']) + '\n')
        response.write('Duration: ' + str(stop['costs']['duration']) + '\n')
        response.write('\n')

    return response
