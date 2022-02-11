"""dataservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from dataservice import api_urls
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    url(r'^ct/api/', include(api_urls), name='api-root'),
    url(r'^ct/api/schema/', SpectacularAPIView.as_view(), name='schema'),
    url(r'^ct/api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'),
    url(r'^ct/admin/', admin.site.urls),
    url(r'^ct/graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [url(r'^ct/api/obtain-auth-token/$', obtain_auth_token)]
