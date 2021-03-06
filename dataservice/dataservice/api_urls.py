from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from data_api.views import UserViewSet, set_user_password, UserProfileViewSet, StudentCourseStructureViewset,\
    StructurePreferredCourseEnrollViewset, TransferringEquivalentCourseViewSet
router = DefaultRouter()

router.register(r'users', UserViewSet, 'user')
router.register(r'profile', UserProfileViewSet, 'profile')
router.register(r'my-course', StudentCourseStructureViewset, 'my-course')
router.register(r'school-course',
                StructurePreferredCourseEnrollViewset, 'school-course')
router.register(r'equivalent-course',
                TransferringEquivalentCourseViewSet, 'equivalent-course')


urlpatterns = [

    url(r'', include(router.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^api-token-auth/', views.obtain_auth_token),

    url(r'^set-password/(?P<pk>\d+)/$', set_user_password, name='set-password'),
]
