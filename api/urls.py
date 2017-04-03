from django.conf.urls import url

from api.views import basic_test

urlpatterns = [
    url(r'^test/', basic_test)
]