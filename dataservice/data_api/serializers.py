from rest_framework import routers, serializers
from data_api.models import UserProfile, UnitOfMeasureCategory, UnitOfMeasure, Dimension, Product, Coord, TimeWindow, OrderItem, InventoryItem, Location, CarrierClass, Carrier, Customer, DeliveryImage, Order, MapOutWay, MapWay, Map, Trip
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from drf_extra_fields.fields import Base64ImageField
import json

ROLE_CHOICES = (
    ('trip_manager', 'TripManager'),
    ('sale_person', 'SalePerson'),
    ('back_officer', 'BackOfficer'),
    ('order_manager', 'OrderManager'),
    ('service_admin', 'ServiceAdmin'),
    ('driver', 'driver')
)


class SetUserPassword(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('password', 'confirm_password')
        write_only_fields = ('password', )
        read_only_fields = (
            'id',
            'is_staff',
            'is_superuser',
            'is_active',
            'date_joined',
        )

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES, write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    group = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password',
                  'confirm_password', 'email', 'role', 'group')
        write_only_fields = ('password', )
        read_only_fields = (
            'id',
            'is_staff',
            'is_superuser',
            'is_active',
            'date_joined',
        )

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        role = validated_data.pop('role')
        user = User.objects.create(**validated_data)

        user_profile = UserProfile.objects.create(user=user, role=role)
        return user

    def get_group(self, obj):
        groups = []
        for group in obj.groups.all():
            groups.append(group.name)
        return groups


class AuthGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
        )
        write_only_fields = ('password', )
        read_only_fields = (
            'id',
            'is_staff',
            'is_superuser',
            'is_active',
            'date_joined',
        )


class AuthUserSortDetailSerializer(serializers.ModelSerializer):
    groups = AuthGroupSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'groups',
        )


class UserDetailsSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'role')
        write_only_fields = ('password', )
        read_only_fields = (
            'id',
            'is_staff',
            'is_superuser',
            'is_active',
            'date_joined',
        )

    def get_role(self, obj):
        groups = []
        for group in obj.groups.all():
            groups.append(group.name)
        if len(groups) > 0:
            return groups[0]


class VrpTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    user = UserDetailsSerializer()

    class Meta:
        model = Token
        fields = ('key', 'user')


class UnitOfMeasureCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasureCategory
        fields = '__all__'


class UnitOfMeasureDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = '__all__'


class UnitOfMeasureSerializer(serializers.ModelSerializer):
    category = UnitOfMeasureCategorySerializer()

    class Meta:
        model = UnitOfMeasure
        fields = ('id', 'name', 'uom_type', 'category', 'rounding', 'factor')


class UnitOfMeasureCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = ('id', 'name', 'uom_type', 'category', 'rounding', 'factor')


class DimensionSerializer(serializers.ModelSerializer):
    width = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()
    length = serializers.SerializerMethodField()

    class Meta:
        model = Dimension
        fields = (
            'id',
            'width',
            'height',
            'length',
        )
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def get_width(self, obj):
        return {'quantity': obj.width, 'uom': obj.uom.name}

    def get_height(self, obj):
        return {'quantity': obj.height, 'uom': obj.uom.name}

    def get_length(self, obj):
        return {'quantity': obj.length, 'uom': obj.uom.name}


class DimensionCreateSerializer(serializers.ModelSerializer):
    width = serializers.FloatField(write_only=True)
    height = serializers.FloatField(write_only=True)
    length = serializers.FloatField(write_only=True)
    uom = serializers.PrimaryKeyRelatedField(
        queryset=UnitOfMeasure.objects.all(), write_only=True)

    class Meta:
        model = Dimension
        fields = ('id', 'width', 'height', 'length', 'uom')


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coord
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class TimeWindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeWindow
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    weight = serializers.SerializerMethodField()
    uom = serializers.SerializerMethodField()
    dimension = DimensionSerializer()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'uom',
            'dimension',
            'weight',
        )
        # exclude = ('created_user','updated_user','created_at','updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def get_weight(self, obj):
        return {'quantity': obj.weight, 'uom': obj.uom_weight.name}

    def get_uom(self, obj):
        return obj.uom.name


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'uom', 'dimension', 'weight', 'uom_weight')
        # exclude = ('created_user','updated_user','created_at','updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data['created_user'] = request.user
        product = Product.objects.create(**validated_data)
        return product


class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name')
        # exclude = ('created_user','updated_user','created_at','updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class OrderItemSerializer(serializers.ModelSerializer):
    uom = serializers.SerializerMethodField()
    product = ProductSimpleSerializer()

    class Meta:
        model = OrderItem
        fields = ('id', 'uom', 'quantity', 'sequence', 'product')
        # exclude = ('created_user','updated_user','created_at','updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def get_uom(self, obj):
        return obj.uom.name


class OrderItemCreateSerializer(serializers.ModelSerializer):
    uom = serializers.PrimaryKeyRelatedField(
        queryset=UnitOfMeasure.objects.all(), write_only=True)

    class Meta:
        model = OrderItem
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data['created_user'] = request.user
        orderitem = OrderItem.objects.create(**validated_data)
        return orderitem


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class LocationSerializer(serializers.ModelSerializer):
    coord = CoordSerializer()
    time_windows = TimeWindowSerializer(many=True)
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Location
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class LocationCreateSerializer(serializers.ModelSerializer):
    coord = serializers.PrimaryKeyRelatedField(queryset=Coord.objects.all(),
                                               write_only=True)
    time_windows = serializers.PrimaryKeyRelatedField(
        queryset=TimeWindow.objects.all(), write_only=True, many=True)
    items = serializers.PrimaryKeyRelatedField(
        queryset=InventoryItem.objects.all(), write_only=True, many=True)

    class Meta:
        model = Location
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class LocationNameSerializer(serializers.ModelSerializer):
    coord = CoordSerializer()

    class Meta:
        model = Location
        fields = ('id', 'name', 'coord')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data['created_user'] = request.user
        location = Location.objects.create(**validated_data)
        return location


class CarrierClassSerializer(serializers.ModelSerializer):
    weight_cap = serializers.SerializerMethodField()
    dimension = DimensionSerializer()

    class Meta:
        model = CarrierClass
        fields = (
            'id',
            'carrier_type',
            'dimension',
            'weight_cap',
        )
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def get_weight_cap(self, obj):
        return {'quantity': obj.weight_cap, 'uom': obj.uom.name}


class CarrierClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarrierClass
        fields = ('id', 'carrier_type', 'dimension', 'weight_cap', 'uom')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class CarrierClassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarrierClass
        fields = (
            'id',
            'carrier_type',
        )
        # exclude = ('created_user','updated_user','created_at','updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class CarrierSerializer(serializers.ModelSerializer):
    carrier_class = CarrierClassTypeSerializer()
    location = LocationNameSerializer()

    class Meta:
        model = Carrier
        fields = ('id', 'name', 'driver', 'carrier_class', 'fuel_cost', 'fuel_cost_type',
                  'service_cost', 'service_cost_type', 'fixed_cost',
                  'fixed_cost_type', 'man_cost', 'man_cost_type', 'location',
                  'is_occupied')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class CarrierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = ('id', 'name', 'driver', 'carrier_class', 'fuel_cost', 'fuel_cost_type',
                  'service_cost', 'service_cost_type', 'fixed_cost',
                  'fixed_cost_type', 'man_cost', 'man_cost_type', 'location',
                  'is_occupied')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data['created_user'] = request.user
        carrier = Carrier.objects.create(**validated_data)
        return carrier


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_delivery_time_windowonly_fields = ('created_user', 'updated_user',
                                                'created_at', 'updated_at')


class CustomerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name')
        # exclude = ('created_user','updated_user','created_at','updated_at')
        read_delivery_time_windowonly_fields = ('created_user', 'updated_user',
                                                'created_at', 'updated_at')


class DeliveryImageSerializer(serializers.ModelSerializer):
    id = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=100))
    image = Base64ImageField()

    class Meta:
        model = DeliveryImage
        fields = ('id', 'image')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data['created_user'] = request.user
        delivery_images = DeliveryImage.objects.create(**validated_data)
        return delivery_images


class OrderSerializer(serializers.ModelSerializer):
    delivery_time_windows = TimeWindowSerializer(many=True)
    items = OrderItemSerializer(many=True)
    source_location = LocationNameSerializer()
    delivery_location = LocationNameSerializer()
    customer = CustomerNameSerializer()

    class Meta:
        model = Order
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class OrderCreateSerializer(serializers.ModelSerializer):
    delivery_images = serializers.ListField(child=Base64ImageField(),
                                            required=False,
                                            write_only=True)
    sign_on_glass = Base64ImageField(required=False)
    end_latitude = serializers.DecimalField(max_digits=9,
                                            decimal_places=6,
                                            required=False)
    end_longitude = serializers.DecimalField(max_digits=9,
                                             decimal_places=6,
                                             required=False)
    receiver = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = Order
        fields = ('id', 'source_location', 'delivery_location', 'customer',
                  'sequence', 'status', 'order_type', 'delivery_date',
                  'delivery_time_windows', 'items', 'delivery_images',
                  'start_latitude', 'start_longitude', 'end_latitude',
                  'end_longitude', 'sign_on_glass', 'receiver', 'remark')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def create(self, validated_data):

        user = None
        request = self.context.get("request")

        if request and hasattr(request, "user"):
            validated_data['created_user'] = request.user
        order = Order.objects.create(**validated_data)
        return order


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    delivery_images = serializers.ListField(child=Base64ImageField(),
                                            required=False,
                                            write_only=True)
    sign_on_glass = Base64ImageField(required=False)
    end_latitude = serializers.DecimalField(max_digits=9,
                                            decimal_places=6,
                                            required=False)
    end_longitude = serializers.DecimalField(max_digits=9,
                                             decimal_places=6,
                                             required=False)
    receiver = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = Order
        fields = ('id', 'source_location', 'delivery_location', 'customer',
                  'sequence', 'status', 'order_type', 'delivery_date',
                  'delivery_time_windows', 'items', 'delivery_images',
                  'start_latitude', 'start_longitude', 'end_latitude',
                  'end_longitude', 'sign_on_glass', 'receiver', 'remark')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def update(self, instance, validated_data):
        if validated_data.get('delivery_images'):
            delivery_images = validated_data.pop('delivery_images')
            images = []
            for image in delivery_images:
                images.append(DeliveryImage.objects.create(image=image))

            instance.delivery_images.set(images)
        if validated_data.get('sign_on_glass'):
            instance.sign_on_glass = validated_data.get('sign_on_glass')
        if validated_data.get('receiver'):
            instance.receiver = validated_data.get('receiver')
        if validated_data.get('start_latitude'):
            instance.start_latitude = validated_data.get('start_latitude')
        if validated_data.get('start_longitude'):
            instance.start_longitude = validated_data.get('start_longitude')
        if validated_data.get('end_latitude'):
            instance.end_latitude = validated_data.get('end_latitude')
        if validated_data.get('end_longitude'):
            instance.end_longitude = validated_data.get('end_longitude')
        if validated_data.get('status'):
            instance.status = validated_data.get('status')
        if validated_data.get('remark'):
            instance.remark = validated_data.get('remark')

        instance.save()
        return instance


class OrderSimpleSerializer(serializers.ModelSerializer):
    number_of_items = serializers.SerializerMethodField()
    customer = CustomerNameSerializer()
    delivery_location = LocationSerializer()

    class Meta:
        model = Order
        exclude = ('items', 'delivery_time_windows', 'created_user',
                   'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def get_number_of_items(self, obj):
        return len(obj.items.all())


class MapOutWaySerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        model = MapOutWay
        fields = ('output_location', 'duration', 'distance')
        # exclude = ('created_user','updated_user','created_at','updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def get_distance(self, obj):
        return {'quantity': obj.distance, 'uom': obj.distance_uom.name}


class MapWaySerializer(serializers.ModelSerializer):
    output_ways = MapOutWaySerializer(many=True)

    class Meta:
        model = MapWay
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class MapSerializer(serializers.ModelSerializer):
    ways = MapWaySerializer(many=True)

    class Meta:
        model = Map
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class MapLocationSerializer(serializers.ModelSerializer):
    coord = CoordSerializer()

    class Meta:
        model = Location
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at',
                   'time_windows', 'items')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class MapOutWayDetailSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    output_location = MapLocationSerializer()

    class Meta:
        model = MapOutWay
        fields = ('id', 'output_location', 'duration', 'distance')
        # exclude = ('created_user','updated_user','created_at','updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def get_distance(self, obj):
        return {'quantity': obj.distance, 'uom': obj.distance_uom.name}


class MapOutWayDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapOutWay
        fields = ('id', 'output_location', 'duration', 'distance',
                  'distance_uom')
        # exclude = ('created_user','updated_user','created_at','updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def get_distance(self, obj):
        return {'quantity': obj.distance, 'uom': obj.distance_uom.name}

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data['created_user'] = request.user
        mapoutway = MapOutWay.objects.create(**validated_data)
        return mapoutway


class MapWayDetailSerializer(serializers.ModelSerializer):
    output_ways = MapOutWayDetailSerializer(many=True)
    source_location = MapLocationSerializer()

    class Meta:
        model = MapWay
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class MapWayDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapWay
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at',
                   'output_ways')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data['created_user'] = request.user
        mapway = MapWay.objects.create(**validated_data)
        return mapway


class MapWayDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapWay
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data['created_user'] = request.user
        ma = Product.objects.create(**validated_data)
        return ma


class MapDetailSerializer(serializers.ModelSerializer):
    ways = MapWayDetailSerializer(many=True)

    class Meta:
        model = Map
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class MapDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class TripSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    carrier_classes = CarrierClassSerializer(many=True, read_only=True)
    source_location = LocationNameSerializer()
    plan_data = serializers.SerializerMethodField()
    carrier = CarrierSerializer()

    class Meta:
        model = Trip
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def get_plan_data(self, obj):
        return json.loads(obj.plan_data or '[]')


class TripCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('id', 'carrier', 'source_location', 'name', 'delivery_date', 'orders',
                  'carrier_classes', 'is_round_trip', 'plan_data', 'plan_type',
                  'mile_in', 'remark')
        # exclude = ('created_user','updated_user','created_at','updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')
