from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls

API_TITLE = 'Support API'
API_DESCRIPTION = 'Web API для взаимодействия техподдержки и клиентов.'


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api-auth/', include('djoser.urls')),
    path('api-auth/', include('djoser.urls.jwt')),
    path('api/v1/', include('api.urls')),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
]
