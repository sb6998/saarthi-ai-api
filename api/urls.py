from django.urls import include, path
from rest_framework import routers
from . import views
from .views import apiViewSet, apiExternalView

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/',apiViewSet.as_view()),
    path('books/', apiViewSet.as_view()),
    path('books/<int:id>', apiViewSet.as_view()),
    path('external-books',apiExternalView.as_view()),
    path('external-books/<int:id>',apiExternalView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]