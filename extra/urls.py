from django.urls import path
from extratest.views import MainView

urlpatterns = [
    path('', MainView.as_view(), name='main_url')
]
