from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, Group
from rolepermissions.roles import assign_role, remove_role

UOM_TYPE_CHOICES = (
    ('bigger', 'Bigger'),
    ('reference', 'Reference'),
    ('smaller', 'Smaller'),
)

COST_TYPE_CHOICES = (
    ('distance', 'Per Distance(km)'),
    ('trip', 'Per Trip'),
    ('day', 'Daily'),
    ('week', 'Weekly'),
    ('month', 'Monthly'),
    ('year', 'Yearly'),
)

ROLE_CHOICES = (
    ('trip_manager', 'TripManager'),
    ('sale_person', 'SalePerson'),
    ('back_officer', 'BackOfficer'),
    ('order_manager', 'OrderManager'),
    ('service_admin', 'ServiceAdmin'),
    ('driver', 'driver')
)


class Company(models.Model):
    name = models.CharField(max_length=200, default="Company")
    max_carrier = models.IntegerField(default=0)
    start_valid_date = models.DateField(default=datetime.now)
    valid_until = models.DateField(default=datetime.now)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user_profile')
    company = models.ForeignKey(Company,
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def save(self, *args, **kwargs):
        remove_role(self.user, self.role)
        assign_role(self.user, self.role)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class UnitOfMeasureCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(UnitOfMeasureCategory,
                                 on_delete=models.CASCADE)
    factor = models.FloatField(default=1.0)
    uom_type = models.CharField(max_length=10, choices=UOM_TYPE_CHOICES)
    rounding = models.IntegerField(default=2)

    def __str__(self):
        return self.name


class Dimension(models.Model):
    width = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    length = models.FloatField(default=0.0)
    uom = models.ForeignKey(UnitOfMeasure,
                            null=True,
                            blank=True,
                            on_delete=models.SET_NULL)
    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="dimension_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="dimension_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.width) + u'x' + str(self.length) + u'x' + str(
            self.height)


class Product(models.Model):
    name = models.CharField(max_length=200)
    weight = models.FloatField(default=0.0)
    uom_weight = models.ForeignKey(UnitOfMeasure,
                                   default=1,
                                   related_name="product_weight_uom",
                                   on_delete=models.SET_DEFAULT)
    uom = models.ForeignKey(UnitOfMeasure,
                            default=1,
                            related_name="product_uom",
                            on_delete=models.SET_DEFAULT)
    dimension = models.ForeignKey(Dimension,
                                  null=True,
                                  blank=True,
                                  on_delete=models.SET_NULL)
    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="product_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="product_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


LOCATION_TYPE_CHOICES = (
    ('customer', 'CUSTOMER'),
    ('warehouse', 'WAREHOUSE'),
)


class Coord(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="coord_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="coord_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.lat) + ',' + str(self.lon)


class TimeWindow(models.Model):
    begin = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="time_window_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="time_window_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.begin) + u' - ' + str(self.end)


class OrderItem(models.Model):
    product = models.ForeignKey(Product,
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL)
    quantity = models.FloatField(default=1.0)
    uom = models.ForeignKey(UnitOfMeasure,
                            null=True,
                            blank=True,
                            on_delete=models.SET_NULL)
    sequence = models.IntegerField(default=0)
    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="order_item_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="order_item_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            'sequence',
        ]

    def __str__(self):
        return str(self.product) + ' ' + str(self.quantity) + str(self.uom)


class InventoryItem(models.Model):
    product = models.ForeignKey(Product,
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL)
    quantity = models.FloatField(default=1.0)
    uom = models.ForeignKey(UnitOfMeasure,
                            null=True,
                            blank=True,
                            on_delete=models.SET_NULL)
    created_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="inventory_item_created_user",
        on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="inventory_item_updated_user",
        on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product) + ' ' + str(self.quantity) + str(self.uom)


class Location(models.Model):
    name = models.CharField(max_length=200)
    coord = models.ForeignKey(Coord,
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL)
    location_type = models.CharField(max_length=10,
                                     choices=LOCATION_TYPE_CHOICES)
    time_windows = models.ManyToManyField(TimeWindow, blank=True)
    items = models.ManyToManyField(InventoryItem,
                                   blank=True,
                                   related_name="location_items")
    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="location_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="location_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CarrierClass(models.Model):
    carrier_type = models.CharField(max_length=50)
    dimension = models.ForeignKey(Dimension,
                                  null=True,
                                  blank=True,
                                  on_delete=models.SET_NULL)
    weight_cap = models.FloatField(default=0.0)
    uom = models.ForeignKey(UnitOfMeasure,
                            null=True,
                            blank=True,
                            on_delete=models.SET_NULL)
    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="carrier_class_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="carrier_class_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.carrier_type) + u'(' + str(self.dimension) + str(
            self.uom) + ' - ' + str(self.weight_cap) + u')'


class Carrier(models.Model):
    name = models.CharField(max_length=50)
    carrier_class = models.ForeignKey(CarrierClass,
                                      null=True,
                                      blank=True,
                                      on_delete=models.SET_NULL)
    driver = models.ForeignKey(UserProfile,
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)

    fuel_cost = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    default=0.0)
    fuel_cost_type = models.CharField(max_length=10,
                                      choices=COST_TYPE_CHOICES,
                                      default='distance')
    service_cost = models.DecimalField(max_digits=10,
                                       decimal_places=2,
                                       default=0.0)
    service_cost_type = models.CharField(max_length=10,
                                         choices=COST_TYPE_CHOICES,
                                         default='year')
    man_cost = models.DecimalField(max_digits=10,
                                   decimal_places=2,
                                   default=0.0)
    man_cost_type = models.CharField(max_length=10,
                                     choices=COST_TYPE_CHOICES,
                                     default='month')
    fixed_cost = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     default=0.0)
    fixed_cost_type = models.CharField(max_length=10,
                                       choices=COST_TYPE_CHOICES,
                                       default='trip')
    is_occupied = models.BooleanField(default=False)
    location = models.ForeignKey(Location,
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL)
    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="carrier_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="carrier_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    mobile = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    locations = models.ManyToManyField(Location, blank=True)
    priority = models.IntegerField(default=0)
    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="customer_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="customer_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


ORDER_TYPE_CHOICES = (
    ('normal', 'NORMAL'),
    ('express', 'EXPRESS'),
)

ORDER_STATUS_CHOICES = (
    ('new', 'NEW'),
    ('loaded', 'LOADED'),
    ('delivered', 'DELIVERED'),
)


class DeliveryImage(models.Model):

    image = models.ImageField(upload_to='delivery_images/',
                              null=True, blank=True)

    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="order_log_car_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="order_log_car_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    sequence = models.IntegerField(default=0)
    customer = models.ForeignKey(Customer,
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL)
    order_type = models.CharField(max_length=10,
                                  choices=ORDER_TYPE_CHOICES,
                                  default='normal')
    status = models.CharField(max_length=10,
                              choices=ORDER_STATUS_CHOICES,
                              default='new')
    delivery_date = models.DateField()
    source_location = models.ForeignKey(Location,
                                        related_name="order_source_location",
                                        default=1,
                                        on_delete=models.SET_DEFAULT)
    delivery_location = models.ForeignKey(Location,
                                          related_name="location_orders",
                                          null=True,
                                          blank=True,
                                          on_delete=models.SET_NULL)
    delivery_time_windows = models.ManyToManyField(TimeWindow, blank=True)
    items = models.ManyToManyField(OrderItem,
                                   blank=True,
                                   related_name="item_orders")
    delivery_images = models.ManyToManyField(DeliveryImage,
                                             blank=True,
                                             related_name="delivery_images_order")
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True,
                                         blank=True,)
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True,
                                          blank=True,)
    end_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True,
                                       blank=True,)
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True,
                                        blank=True,)

    sign_on_glass = models.ImageField(upload_to='sign_on_glass_images/', null=True,
                                      blank=True,)

    receiver = models.CharField(max_length=200, null=True,
                                blank=True,)
    remark = models.TextField(
        null=True,
        blank=True,
    )

    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="order_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="order_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            'sequence',
        ]

    def __str__(self):
        return str(self.delivery_date) + '-' + str(self.customer)


class MapOutWay(models.Model):
    output_location = models.ForeignKey(Location,
                                        related_name='to',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)
    distance = models.FloatField(default=1.0)
    distance_uom = models.ForeignKey(UnitOfMeasure,
                                     related_name="+",
                                     null=True,
                                     blank=True,
                                     on_delete=models.SET_NULL)
    duration = models.TimeField(null=True, blank=True)
    conversion_factor = models.FloatField(default=1.0)

    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="map_out_way_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="map_out_way_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.output_location.name)


class MapWay(models.Model):
    source_location = models.ForeignKey(Location,
                                        related_name='source',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)
    output_ways = models.ManyToManyField(MapOutWay)

    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="map_way_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="map_way_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.source_location.name)


class Map(models.Model):
    name = models.CharField(max_length=200)
    ways = models.ManyToManyField(MapWay)
    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="map_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="map_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


PLAN_TYPE_CHOICES = (
    ('cost_rank', 'COST'),
    ('dist_rank', 'DISTANCE'),
    ('time_rank', 'TIME'),
)


class Trip(models.Model):
    name = models.CharField(max_length=200)
    carrier = models.ForeignKey(Carrier,
                                null=True,
                                blank=True,
                                related_name="trip_carrier",
                                on_delete=models.SET_NULL)
    delivery_date = models.DateField()
    source_location = models.ForeignKey(Location,
                                        related_name="trip_source_location",
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)
    is_round_trip = models.BooleanField(default=True, )
    orders = models.ManyToManyField(Order,
                                    blank=True,
                                    related_name="trip_orders")
    carrier_classes = models.ManyToManyField(
        CarrierClass,
        blank=True,
        related_name="trip_carrier_classes",
    )
    plan_data = models.TextField(
        null=True,
        blank=True,
    )
    plan_type = models.CharField(max_length=10,
                                 choices=PLAN_TYPE_CHOICES,
                                 default='cost_rank')
    mile_in = models.FloatField(null=True,
                                blank=True,)
    remark = models.TextField(
        null=True,
        blank=True,
    )
    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="trip_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="trip_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.delivery_date) + '-' + str(self.name)
