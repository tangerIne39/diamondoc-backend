from django.urls import path

from .views import *

urlpatterns = [
    # ------------yxy------------
    path('login', login),
    path('get_user', get_user),

    # ------------wlc------------

    # ------------end------------
]
