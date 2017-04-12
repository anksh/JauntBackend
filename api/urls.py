from django.conf.urls import include, url

from api.routes import *


jaunt_urls = [
    url(r'^create/', create_jaunt),
    url(r'(?P<id>[0-9]+)', get_jaunt),
    url(r'^join/', join_jaunt),
    url(r'^leave/', leave_jaunt)
]
user_urls = [
    url(r'^create/', create_user),
    url(r'(?P<user_id>[(0-9a-zA-Z)]+)', get_user)
]
urlpatterns = [
    url(r'^jaunt/', include(jaunt_urls)),
    url(r'^photo/', add_photo),
    url(r'^user/', include(user_urls))

]
