from django.conf.urls import include, url

from api.routes import *


jaunt_urls = [
    url(r'^create/', create_jaunt),
    url(r'(?P<id>[0-9]+)', get_jaunt),
    url(r'^join/', join_jaunt)
]
urlpatterns = [
    url(r'^jaunt/', include(jaunt_urls)),
    url(r'^photo/', add_photo)

]
