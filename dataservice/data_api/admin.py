from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from data_api.models import *
from rangefilter.filters import DateRangeFilter


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.name != "id"
        ]
        super(CustomModelAdmin, self).__init__(model, admin_site)


class CustomSaveModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.name != "id"
        ]
        self.exclude = ['created_user', 'updated_user']
        super(CustomSaveModelAdmin, self).__init__(model, admin_site)

    def save_model(self, request, obj, form, change):
        if obj is None:
            obj.created_user = request.user
        obj.updated_user = request.user
        obj.save()


class CompanyAdmin(CustomModelAdmin):
    search_fields = ('max_carrier', 'start_date', 'end_date')


class UserProfileAdmin(CustomModelAdmin):
    search_fields = ('company', 'role')


class UnitOfMeasureCategoryAdmin(CustomModelAdmin):
    search_fields = ('name', )


class UnitOfMeasureAdmin(CustomModelAdmin):
    search_fields = ('name', )
    list_filter = ('category', )


class DimensionAdmin(CustomSaveModelAdmin):
    search_fields = (
        'uom__name',
        'created_user__username',
        'updated_user__username',
    )
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


class ProductAdmin(CustomSaveModelAdmin):
    search_fields = (
        'name',
        'uom',
        'created_user__username',
        'updated_user__username',
    )
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


class CoordAdmin(CustomSaveModelAdmin):
    search_fields = (
        'created_user__username',
        'updated_user__username',
    )
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


class TimeWindowAdmin(CustomSaveModelAdmin):
    search_fields = (
        'created_user__username',
        'updated_user__username',
    )
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


class InventoryItemAdmin(CustomSaveModelAdmin):
    search_fields = (
        'created_user__username',
        'updated_user__username',
    )
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


class OrderItemAdmin(CustomModelAdmin):
    search_fields = (
        'product',
        'uom',
        'created_user__username',
        'updated_user__username',
    )
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


class LocationAdmin(CustomSaveModelAdmin):
    search_fields = (
        'name',
        'location_type',
        'created_user__username',
        'updated_user__username',
    )
    list_filter = (
        'location_type',
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


class CarrierClassAdmin(CustomSaveModelAdmin):
    search_fields = (
        'carrier_type',
        'uom',
        'created_user__username',
        'updated_user__username',
    )
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


class CarrierAdmin(CustomSaveModelAdmin):
    search_fields = (
        'name',
        'carrier_class',
        'location',
        'created_user__username',
        'updated_user__username',
    )
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


class CustomerAdmin(CustomSaveModelAdmin):
    search_fields = (
        'name',
        'address',
        'phone',
        'mobile'
        'created_user__username',
        'updated_user__username',
    )
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


class MapOutWayAdmin(CustomSaveModelAdmin):
    search_fields = (
        'output_location',
        'created_user__username',
        'updated_user__username',
    )
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


class MapWayAdmin(CustomSaveModelAdmin):
    search_fields = (
        'source_location',
        'created_user__username',
        'updated_user__username',
    )
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


class MapAdmin(CustomSaveModelAdmin):
    search_fields = (
        'name',
        'created_user__username',
        'updated_user__username',
    )


class TripInline(admin.TabularInline):
    model = Trip.orders.through


class TripAdmin(CustomSaveModelAdmin):
    inlines = [TripInline]

    fields = ('name', 'delivery_date', 'source_location', 'carrier')

    search_fields = (
        'name',
        'delivery_date',
        'carrier'
        'created_user__username',
        'updated_user__username',
    )
    list_filter = (
        ('delivery_date', DateRangeFilter),
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


class OrderInline(admin.TabularInline):
    model = Order.items.through
    extra = 1


class OrderAdmin(CustomSaveModelAdmin):
    inlines = [
        OrderInline,
    ]
    fields = (
        'sequence',
        'customer',
        'delivery_date',
        'delivery_location',
        'delivery_time_windows',
    )
    search_fields = (
        'created_user__username',
        'updated_user__username',
    )
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


admin.site.register(UnitOfMeasureCategory, UnitOfMeasureCategoryAdmin)
admin.site.register(UnitOfMeasure, UnitOfMeasureAdmin)
admin.site.register(Dimension, DimensionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Coord, CoordAdmin)
admin.site.register(TimeWindow, TimeWindowAdmin)
#admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(CarrierClass, CarrierClassAdmin)
admin.site.register(Carrier, CarrierAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(MapOutWay, MapOutWayAdmin)
admin.site.register(MapWay, MapWayAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Company, CompanyAdmin)
