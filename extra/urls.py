from django.urls import path
from extratest.views import (ChooseNumberOfExtrasensesView, MainGameFirstWindowView,
                             MainGameSecondWindowView, )

urlpatterns = [
    path('', ChooseNumberOfExtrasensesView.as_view(), name='start_url'),
    path('get_ready', MainGameFirstWindowView.as_view(), name='maingame_first_window_url'),
    path('my_number_was', MainGameSecondWindowView.as_view(), name='maingame_second_window_url'),
]
