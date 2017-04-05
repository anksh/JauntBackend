from django.conf.urls import include, url

from api.routes import *


jaunt_urls = [
    url(r'^create/', create_jaunt)
]
urlpatterns = [
    url(r'^jaunt/', include(jaunt_urls))
]
