from django.urls import re_path

from . import views

#: namespace use requirements
app_name = 'health'


urlpatterns = [
    re_path('^status/$', views.StatusView.as_view(), name='status'),
    re_path('^healthz/$', views.HealthView.as_view(), name='health')
]
