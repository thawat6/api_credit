from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from data_api.views import ProductViewSet, UnitOfMeasureCategoryViewSet, UnitOfMeasureViewSet, \
    DimensionViewSet, CoordViewSet, TimeWindowViewSet, OrderItemViewSet, UserViewSet,\
    InventoryItemViewSet, LocationViewSet, CarrierClassViewSet, CarrierViewSet, \
    CustomerViewSet, OrderViewSet, MapOutWayViewSet, MapWayViewSet, MapViewSet, \
    TripViewSet, OrderInstanceItemViewSet, OrderInstanceLocationViewSet, set_user_password,\
    LocationInstanceItemViewSet, TripInstanceOrderViewSet, TripInstanceCarrierClassViewSet, \
    exports_trip_detail, MapDetailViewSet, MapWayDetailViewSet, MapOutWayDetailViewSet, \
    exports_plan_detail, exports_plan_detail_api
router = DefaultRouter()
router.register(r'products', ProductViewSet, 'product')
router.register(r'unit-of-measure-categories',
                UnitOfMeasureCategoryViewSet, 'unit-of-measure-categories')
router.register(r'unit-of-measures', UnitOfMeasureViewSet, 'unit-of-measure')
router.register(r'dimensions', DimensionViewSet, 'dimension')
router.register(r'coords', CoordViewSet, 'coord')
router.register(r'time-windows', TimeWindowViewSet, 'time-window')
router.register(r'order-items', OrderItemViewSet, 'order-item')
router.register(r'inventory-items', InventoryItemViewSet, 'inventory-item')
router.register(r'locations', LocationViewSet, 'location')
router.register(r'carrier-classes', CarrierClassViewSet, 'carrier-class')
router.register(r'carriers', CarrierViewSet, 'carrier')
router.register(r'customers', CustomerViewSet, 'customer')
router.register(r'orders', OrderViewSet, 'order')
router.register(r'map-out-ways', MapOutWayViewSet, 'map-out-way')
router.register(r'map-ways', MapWayViewSet, 'map-way')
router.register(r'maps', MapViewSet, 'map')

router.register(r'map-out-ways-detail',
                MapOutWayDetailViewSet, 'vrp-map-out-way')
router.register(r'map-ways-detail', MapWayDetailViewSet, 'vrp-map-way')
router.register(r'maps-detail', MapDetailViewSet, 'vrp-map')

router.register(r'trips', TripViewSet, 'trip')
router.register(r'users', UserViewSet, 'user')


urlpatterns = [
    url(r'^carrier-classes/(?P<pk>.*)/$', CarrierClassViewSet.as_view(
        {'get': 'retrieve_by_name', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='carrier-class-detail-by-carrier-type'),
    url(r'^unit-of-measures/(?P<pk>.*)/$', UnitOfMeasureViewSet.as_view(
        {'get': 'retrieve_by_name', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='unit-of-measure-detail-by-name'),
    url(r'^orders/(?P<order_id>[^/.]+)/items/$', OrderInstanceItemViewSet.as_view(
        {'get': 'list'}), name='order-list-item-list'),
    url(r'^orders/(?P<order_id>[^/.]+)/delivery-locations/$',
        OrderInstanceLocationViewSet.as_view({'get': 'list'}), name='order-list-location-list'),
    url(r'^locations/(?P<location_id>[^/.]+)/items/$', LocationInstanceItemViewSet.as_view(
        {'get': 'list'}), name='location-list-item-list'),
    url(r'^trips/(?P<trip_id>[^/.]+)/orders/$', TripInstanceOrderViewSet.as_view(
        {'get': 'list'}), name='trip-list-order-list'),
    url(r'^trips/(?P<trip_id>[^/.]+)/carrier-classes/$', TripInstanceCarrierClassViewSet.as_view(
        {'get': 'list'}), name='trip-list-carrier-class-list'),
    url(r'', include(router.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^trips/(?P<trip_id>[^/.]+)/exports/(?P<format_param>.*)/$',
        exports_trip_detail, name='exports-trip-detail'),
    url(r'^trips/(?P<trip_id>[^/.]+)/exports-plan-api/(?P<format_param>.*)/$',
        exports_plan_detail_api, name='exports-plan-detail-api'),
    url(r'^trips/(?P<trip_id>[^/.]+)/exports-plan/(?P<format_param>.*)/$',
        exports_plan_detail, name='exports-plan-detail'),
    url(r'^set-password/(?P<pk>\d+)/$', set_user_password, name='set-password'),
]
